import zmq
from gaia.log.log import Log

class SendRecv(object):
    ''' A base class for sending and receiving Tasks.

        A Mgr will     send   jobs and receive results.
        A Worker will receive jobs and send    results back to the Mgr.
    '''
    term_timeout = 2 * 1000   # 2 secs: time for context.term() to wait before discarding messages and quiting (in milliseconds)

    def __init__(self, is_master, config):
        self.is_master = is_master # is_master indicates if this process sends commands or actions them.
        self.config = config
        self._log = Log.get_logger(self)

    def setup_zmq(self, send_socket, recv_socket, context):
        self._log.enter()

        if self.is_master:
            # NOTE: use explicit call so that this can be used in multiple inheritance
            SendRecv._setup_master(self, send_socket, recv_socket, context)
        else:
            SendRecv._setup_servant(self, send_socket, recv_socket, context)

    def _setup_master(self, send_socket, recv_socket, context):
        ' use BIND at the master end: must be ONLY ONE MASTER '
        # looks like zmq ends need to be in bind/connect pairs
        self._log.enter()
        self._log.info('sending on bind', send_socket=send_socket)
        self._send_socket = context.socket(zmq.PUSH)
        self._send_socket.bind(send_socket)
        #self._send_socket.setsockopt(zmq.LINGER, self.term_timeout)

        self._log.info('receiving on bind', recv_socket=recv_socket)
        self._receive_socket = context.socket(zmq.PULL)
        self._receive_socket.bind(recv_socket)
        #self._receive_socket.setsockopt(zmq.LINGER, self.term_timeout)
        self._log.exit()

    def _setup_servant(self, send_socket, recv_socket, context):
        ' use CONNECT at the slave ends: there may be many slaves '
        self._log.enter()
        self._log.info('sending on connect', send_socket=send_socket)
        self._send_socket = context.socket(zmq.PUSH)
        self._send_socket.connect(send_socket)
        #self._send_socket.setsockopt(zmq.LINGER, self.term_timeout)

        self._log.info('receiving on connect', recv_socket=recv_socket)
        self._receive_socket = context.socket(zmq.PULL)
        self._receive_socket.connect(recv_socket)
        #self._receive_socket.setsockopt(zmq.LINGER, self.term_timeout)
        self._log.exit()

    def teardown_zmq(self):
        self._log.enter()

        self._send_socket.close()
        self._receive_socket.close()

        self._log.exit()

    def register_with_poller(self, poller):
        self._log.debug('registering receive socket with Poller', socket=self._receive_socket)
        poller.register(self._receive_socket, zmq.POLLIN)

    def is_msg(self, socks):
        ' have we received a message (on our receive sockets)? '
        # socks = dict(poller.poll())
        return socks.get(self._receive_socket) == zmq.POLLIN

    def send(self, msg, **kwargs):
        ''' send messages on the send socket

            kwargs can be any standard zmq options, eg:
                flags=zmq.NOBLOCK
        '''
        self._send_socket.send(msg, **kwargs)

    def recv(self, **kwargs):
        ''' receive messages from the receive side.

            kwargs can be any standard zmq options, eg:
                flags=zmq.NOBLOCK
        '''
        msg = self._receive_socket.recv(**kwargs)
        return msg
