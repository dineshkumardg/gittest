from gaia.task.msg.msg import Msg

class StatusMsg(Msg):
    def __init__(self, **status_fields):
        Msg.__init__(self, msg_type='STATUS', **status_fields)
