from gaia.task.msg.msg import Msg

class _ReqReply(Msg):
    def __init__(self, is_request, msg_type, **msg_data):
        ' A base class for Request or Reply messages. '
        Msg.__init__(self, msg_type, **msg_data)
        self._msg_data['_is_request'] = is_request

    def is_request(self):
        return self._msg_data['_is_request']

    def is_reply(self):
        return not self._msg_data['_is_request']

class Request(_ReqReply):
    def __init__(self, request_type, **request_data):
        ''' A class for Request messages.

            msg_type is the type of the request.
            msg_data is any fields in the message
        '''
        _ReqReply.__init__(self, True, request_type, **request_data)
