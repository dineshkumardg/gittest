import os
import sys
import time
import logging
import zmq
import readline
from gaia.log.log import Log
from gaia.config.config import get_config 
from gaia.task.manageable import Manageable
from gaia.task.msg.status_msg import StatusMsg

class Admin(Manageable):
    log_name = 'admin'
    management_topic = '_DONT_LISTEN_'   # not used

    def __init__(self, config):
        self.config = config
        fname = Log.configure_logging(self.log_name, config)

        print '=== ADMIN STARTED with config:\n', str(config)
        print "... logging to file: ", fname
        self._log = Log.get_logger(self)

        Manageable.__init__(self)
    
    def complete(self, text, state):
        # function for tab completion in interactive mode
        COMMANDS = ['ingest_worker', 'egest_worker', 'ingest_mgr', 'egest_mgr']
        for cmd in COMMANDS:
            if cmd.startswith(text):
                if not state:
                    return cmd
                else:
                    state -= 1

    def run(self, interact=True, commands=None):
        context = self._setup_zmq(config.management_sockets)
        time.sleep(1)
        try:
            if interact == True:
                self.handle_commands()
            else:
                self.handle_commands_without_interact(commands)

        except zmq.ZMQError, e:
            logging.error('ERROR: Admin: terminated with messaging error: "%s"' % str(e))
        except Exception, e:
            logging.error('ERROR: Admin: terminated with error: "%s"' % str(e))
        
        self._log.info('about to shutdown ...')
        self._teardown_zmq(context)

        self._log.info('END    --------------------------------')
    
    def handle_commands_without_interact(self, commands):
        # support a list of commands from arguments []. e.g: [topic] [command] [topic] [command]...
        time.sleep(3) # Because slow start, to avoid losing msg, here wait a certain time after start PUB socket. 

        for i in range (len(commands)/2):
            topic = commands[i*2]
            command = commands[i*2+1]
            logging.info('... Admin: issuing command "%s", on topic "%s"' % (command, topic))
            Manageable.send(self, topic, command)
            time.sleep(1)

    def handle_commands(self):
        self.print_commands()
        
        poller = zmq.Poller()
        Manageable.register_with_poller(self, poller)
        poller.register(sys.stdin, zmq.POLLIN)

        exit = False
        while not exit:
             # TODO: 1. No value => interleave OK, input history/tab completion not working. 
             # 2. Set value => mgr interleave not works perfectly, input OK.  Need improve in future, multi-process?
            socks = dict(poller.poll(10))  
            if Manageable.is_msg(self, socks):  # get reply from mgr/worker
                topic, text = self._sub_socket.recv_multipart()
                print StatusMsg.decode(text)
            else:    # handle command from stdin
                text = raw_input('Enter Command (q=quit) > ')
                if text == 'q':
                    exit = True
                else:
                    parts = text.split(' ')

                    if len(parts) != 2:
                        print 'please enter a topic; a space; then a command, eg "ingest_worker die", not "%s"' % text
                    else:
                        print
                        topic, command = parts
                        logging.info('... Admin: issuing command "%s", on topic "%s"' % (command, topic))
                        Manageable.send(self, topic, command)

    def _setup_zmq(self, management_sockets):
        context = zmq.Context()

        pub_socket = management_sockets['command']['send'] 
        sub_socket = management_sockets['status']['recv']

        Manageable.setup_zmq_master(self, pub_socket, sub_socket, context)

        return context

    def _teardown_zmq(self, context):
        self._log.enter()

        time.sleep(1) # was reqd to allow zmq to flush buffers, etc (?) # don't think is necessary anymore (ie infinite linger is default) TODO: review

        Manageable.teardown_zmq(self)

        context.term()  # WARNING: on older zmq, this hangs.
        #context.destroy(linger=2*1000)  # Need investigae why the destroy not working?
        self._log.exit()

    def print_commands(self):
        print
        print 'Topics'
        print '------'
        print '\tingest_mgr'
        print '\tingest_worker'
        print '\tegest_worker'
        print '\tegest_mgr'
        print
        print 'Commands'
        print '--------'
        print '\tstatus'
        print '\tdie'
        print
        print 'WARNING: Only kill any Manager AFTER all the workers have died!'
        print
        print 'Use a management-topic followed by a command, eg:'
        print '\t ingest_worker status'
        print '\t ingest_worker die'
        print '\t egest_mgr die'
        print '\t test status'

if __name__ == '__main__':
    try:
        config_name = sys.argv[1] 
        arg_list = sys.argv
        commands = arg_list[2:] # commands from arguments
    except IndexError, e:
        print 'please supply a config name, eg py admin.py TUSH_LINUX'
        sys.exit(1)

    if len(commands)%2 != 0:
        print 'Arguments must have same number of topics and commands, not "%s"' % commands
        print 'Support a list of commands. e.g. [config] [topic] [command] [topic] [command]...'
        sys.exit(1)

    config = get_config(config_name)
    pid = os.getpid()
    print "Staring Admin with pid:", pid
    #print 'config:', config_name

    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename=',admin.log', filemode='w')
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    admin = Admin(config)
    
    # set up interactive mode command line
    readline.parse_and_bind("tab: complete")
    readline.set_completer(admin.complete)

    if commands != []:
        admin.run(interact=False,commands=commands)
    else:
        admin.run()
    print 'FINISHED.'
