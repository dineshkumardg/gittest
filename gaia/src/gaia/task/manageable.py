import zmq
from gaia.log.log import Log

# https://github.com/zeromq/pyzmq/issues/102
# http://api.zeromq.org/2-1:zmq-setsockopt#toc15
# ZMQ_LINGER: Set linger period for socket shutdown
# The ZMQ_LINGER option shall set the linger period for the specified socket. The linger period determines how long pending messages which have yet to be sent to a peer shall linger in memory after a socket is closed with zmq_close(3), and further affects the termination of the socket's context with zmq_term(3). The following outlines the different behaviours:

class Manageable(object):
    ''' A base class for Manageable Zmq Processes
        A Manageable Process handles mangement requests, such as status, die, etc.

        A Mamageable may be in charge (is_master, ie sending commands) or sub-serviant
    '''
    status_reply_topic = 'status' # this is the "reply channel" for status messages (from servants)
    term_timeout = 2 * 1000   # 2 secs: time for context.term() to wait before discarding messages and quiting (in milliseconds)

    def __init__(self):
        try:
            self._log   # TODO: these all need their own names to get the right class name on output :( ?
        except AttributeError, e:
            self._log = Log.get_logger(self)

    def setup_zmq_master(self, pub_socket, sub_socket, context):
        ' set up sockets to be the master, ie sending management commands . '
        self._log.enter()
        topic = self.status_reply_topic # note topic!
        self._log.info('MASTER: sending commands (pub) on', pub_socket=pub_socket)
        self._log.info('MASTER: receive status messages (sub) on', sub_socket=sub_socket, topic=topic) 

        self._pub_socket = context.socket(zmq.PUB)
        #self._pub_socket.connect(pub_socket)
        self._pub_socket.setsockopt(zmq.LINGER, self.term_timeout)
        self._pub_socket.bind(pub_socket)   # in the _master_ case, there's only ONE publisher (ie of commands), so we use bind here.

        self._sub_socket = context.socket(zmq.SUB)
        self._sub_socket.bind(sub_socket)
        self._sub_socket.setsockopt(zmq.LINGER, self.term_timeout)
        self._sub_socket.setsockopt(zmq.SUBSCRIBE, topic)
        self._log.exit()

    # Note: we want multiple publishers, so we're using connect() (bind disallows this), hence we can only have one subscriber! :( 
    # bind = 1 at end of message-queue; connect = many at end of message-queue (?)
    # I think we need a broker for multiple publishers AND subscribers. TODO
    def setup_zmq_slave(self, topic, pub_socket, sub_socket, context):
        ' set up sockets to be the servant ie actioning management commands . '
        self._log.enter()
        self._log.info('SLAVE: sending status replies (pub) on', pub_socket=pub_socket)
        self._log.info('SLAVE: receive management commands (sub) on', sub_socket=sub_socket, commands_topic=topic) 

        self._pub_socket = context.socket(zmq.PUB)
        self._pub_socket.setsockopt(zmq.LINGER, self.term_timeout)
        self._pub_socket.connect(pub_socket)    # there will be many slaves, so we use connect here (to avoid "address is already in use".
        #self._pub_socket.bind(pub_socket)

        self._sub_socket = context.socket(zmq.SUB)
        self._sub_socket.connect(sub_socket)
        self._sub_socket.setsockopt(zmq.LINGER, self.term_timeout)
        self._sub_socket.setsockopt(zmq.SUBSCRIBE, topic)
        self._log.exit()

    def teardown_zmq(self,):
        self._log.enter()

        self._pub_socket.close()
        self._sub_socket.close()

        self._log.exit()

    def register_with_poller(self, poller):
        ' Register incoming sockets so that we can receive admin requests '
        poller.register(self._sub_socket, zmq.POLLIN)

    def is_msg(self, socks):
        ' have we received an admin request message (on our receive sockets)? '
        # socks = dict(poller.poll())
        #return socks.get(self._pub_socket) == zmq.POLLIN
        self._log.info('checking for our msgs', socks=socks)
        return socks.get(self._sub_socket) == zmq.POLLIN

    def send(self, topic, msg, **kwargs):
        ''' send command messages on the management socket with a topic.
            kwargs can be any standard zmq options, eg: flags=zmq.NOBLOCK
        '''
        #self._pub_socket.send(msg, **kwargs)
        self._log.info('Publishing multipart message', topic=topic, msg=msg)
        self._pub_socket.send_multipart([topic, msg])

    def recv(self, **kwargs):
        ''' receive status messages.
            kwargs can be any standard zmq options, eg: flags=zmq.NOBLOCK
        '''
        #msg = self._sub_socket.recv(**kwargs)
        topic, msg = self._sub_socket.recv_multipart(**kwargs)
        self._log.info('Received (subscribed to) multipart message', topic=topic, msg=msg)
        return msg
