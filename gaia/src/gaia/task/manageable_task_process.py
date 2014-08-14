from gaia.task.msg.status_msg import StatusMsg
from gaia.task.manageable import Manageable


class ManageableTaskProcess(Manageable):
    ''' This class provides default Management behaviour for Task processes
        (ie Mgr or Worker, which are both manageable "slaves").
        Subclasses MUST provide a status() method'''

    def __init__(self):
        Manageable.__init__(self)

    def handle_management(self):
        topic, msg = self._sub_socket.recv_multipart() # args# noblock?

        self._log.debug('_handle_management(): ', topic=topic, msg=msg)
        return self.do_management(msg)

    def do_management(self, management_command):
        self._log.info('_do_management(): command: ' + str(management_command))
        dying = False

        if management_command == 'die':
            self._log.info('*** Exiting: asked to DIE ***')

            _status_fields = self.status()
            msg = StatusMsg(status='DYING', **_status_fields)

            # TODO: add a STARTING msg?
            self._log.info('--> sending status "%s"' % msg)
            Manageable.send(self, self.status_reply_topic, msg.encode())

            dying = True

        elif management_command == 'status':
            _status_fields = self.status()
            msg = StatusMsg(status='alive', **_status_fields)

            self._log.info('--> sending status "%s"' % msg)
            Manageable.send(self, self.status_reply_topic, msg.encode())
        else:
            self._log.info('*** IGNORING command %s ***' % str(management_command))

        return dying
 
    #def status(self):
        #' return a status dictionary # Note: do NOT use the key: "status" '
        #return status_dict
