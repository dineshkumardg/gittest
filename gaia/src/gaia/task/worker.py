import os
import time
import socket
import traceback
import zmq
from abc import abstractmethod
from gaia.log.log import Log
from gaia.error import GaiaCodingError
from gaia.task.msg.job_request import JobRequest
from gaia.task.msg.job_reply import OkReply, TryAgainReply, FailedReply
from gaia.task.send_recv import SendRecv
from gaia.task.manageable_task_process import ManageableTaskProcess

class Worker(SendRecv, ManageableTaskProcess):
    process_name = 'worker' # override this please (also used as a log_name and management_topic)

    # return statuses for do() method:
    OK = 1
    TRY_AGAIN = 2
    FAILED = 3

    def __init__(self, job_sockets, config):
        self.config = config
        log_name = self.process_name
        fname = Log.configure_logging(log_name, config, multi_process=True)

        print '=== WORKER STARTED with job_sockets="', str(job_sockets) ,'", config=', str(config)
        print "... logging to file: ", fname
        self._log = Log.get_logger(self)
        self._log.info('='*79)
        self._log.info('=== WORKER STARTED with :', job_sockets=job_sockets)
        self._log.info('config:...')
        self._log.info(str(config))
        self._log.info('-'*79)

        SendRecv.__init__(self, is_master=False, config=config)
        ManageableTaskProcess.__init__(self)

        self.job_sockets = job_sockets
        self.management_sockets = config.management_sockets

        self._id = str(os.getpid())
        self._hostname = socket.getfqdn()
        self._num_requests = 0

    def run(self):    
        ''' run this worker.

            You must call this to start message-processing.
            This will run forever (until the process is terminated).
        '''
        self._log.info('START  --------------------------------', id=self._id)
        context = self._setup_zmq()

        try:
            self._handle_msgs()
        except zmq.ZMQError, e:
            #if e.strerror == 'Context was terminated':  # eg by Ctrl-C/SIGTERM
            self._log.error('ERROR: Worker: terminated with messaging error: "%s"' % str(e))
        except Exception, e:
            self._log.error('ERROR: Worker: terminated with error: "%s" \n Stacktrace:\n%s' % (str(e), traceback.format_exc()))
        except (KeyboardInterrupt, SystemExit), e:
            self._log.error('terminated with KeyboardInterrupt.')
                
        self._log.info('about to shutdown ...')
        self._teardown_zmq(context)
        self._log.info('END    --------------------------------', id=self._id)

    def _handle_msgs(self):
        self._log.enter()
        poller = zmq.Poller()
        SendRecv.register_with_poller(self, poller)
        ManageableTaskProcess.register_with_poller(self, poller)
        exit = False
        while not exit:
            self._log.info('-' * 60)
            self._log.info('--- LOOP: waiting for work and/or management requests ...')
            socks = dict(poller.poll())  # block; waiting for jobs or admin commands

            if ManageableTaskProcess.is_msg(self, socks):
                exit = self.handle_management()

            if not exit:
                if SendRecv.is_msg(self, socks):
                    self._handle_job()

        self._log.exit()

    def _handle_job(self):
        self._log.enter()
        request_msg = SendRecv.recv(self)
        job_request = JobRequest.decode(request_msg)    # WARNING: it's possible that this does NOT return a JobReqyest type! TODO: add check in JobRequest.decode?

        self._log.debug('got job: ', job_request=job_request)

        try:
            status = self.do(job_request)
    
            if status == self.OK:
                reply = OkReply(request_msg)
            elif status == self.FAILED:
                reply = FailedReply(request_msg)
            else:
                if status == self.TRY_AGAIN:
                    reply = TryAgainReply(request_msg)
                else:
                    raise GaiaCodingError('invalid status for a reply from a worker "%s"!' % str(status))
        except IndexError as e:  # http://jira.cengage.com/browse/EG-570
            self._log.warning(e)
            reply = FailedReply(request_msg)

        self._log.debug('done. Sending reply => ' + str(reply))
        SendRecv.send(self, reply.encode())

        self._num_requests += 1
        self._log.exit()

    @abstractmethod
    def do(self, job_request):
        ' handle a JobRequest and return a job-status: OK, FAILED or TRY_AGAIN '
        return self.OK # or self.TRY_AGAIN or self.FAILED

    def _setup_zmq(self):
        context = zmq.Context()

        send_socket = self.job_sockets['reply']['send']
        recv_socket = self.job_sockets['request']['recv']
        SendRecv.setup_zmq(self, send_socket, recv_socket, context)
        self._log.info('receiving jobs on', recv_socket=recv_socket)
        self._log.info('sending replies to jobs on', send_socket=send_socket)

        management_topic = self.process_name
        pub_socket = self.management_sockets['status']['send']
        sub_socket = self.management_sockets['command']['recv']
        ManageableTaskProcess.setup_zmq_slave(self, management_topic, pub_socket, sub_socket, context)

        return context

    def _teardown_zmq(self, context):
        self._log.enter()
        # Note: maybe send a "I'm dying" status message here?

        time.sleep(1) # was reqd to allow zmq to flush buffers, etc (?) # don't think is necessary anymore (ie infinite linger is default) TODO: review

        ManageableTaskProcess.teardown_zmq(self)
        SendRecv.teardown_zmq(self)

        context.term()  # WARNING: hangs in older zeromq versions (fixed in 3.2)
        #context.destroy(linger=0)  # TODO: linger param?
        self._log.exit()

    def status(self):
        ' return a status dictionary # Note: do NOT use the key: "status" '
        _status = {
            'type': 'WORKER', 
            'id': self._id,
            'hostname': self._hostname,
            'num_requests': self._num_requests,
        }
        return _status
