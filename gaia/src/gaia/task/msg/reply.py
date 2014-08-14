from gaia.task.msg.request import _ReqReply, Request

class Reply(_ReqReply):
    ''' A class for Reply messages

        replies are always in response to a request, and this request
        is included in the reply message (as the original encoded msg).
    '''

    def __init__(self, reply_to_encoded_request, reply_type='REPLY', **reply_data):
        # not sure if we need reply_type??.. TODO remove?
        reply_data['_reply_to_request'] = reply_to_encoded_request
        _ReqReply.__init__(self, False, reply_type, **reply_data)

    def request(self):
        ' return the original Request message that this is a repsonse to '
        return Request.decode(self._reply_to_request)
