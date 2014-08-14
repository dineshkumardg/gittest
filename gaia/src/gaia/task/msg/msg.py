import cPickle as pickle

class Msg:
    def __init__(self, msg_type, **msg_data):
        self._msg_type = msg_type
        self._msg_data = msg_data

    def msg_type(self):
        return self._msg_type

    def __getattr__(self, attr):
        try:
            return self.__dict__['_msg_data'][attr]
        except KeyError, e:
            raise AttributeError(attr)

    def __eq__(self, other):
        return self._msg_type == other._msg_type and \
               self._msg_data == other._msg_data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        # Note: this is just for logging and debugging.
        # use encode() to get an encoded Msg, DO NOT USE THIS for that purpose PLEASE!
        #return 'Msg: msg_type="%s", msg_data="%s"' % (self._msg_type, str(self._msg_data))
        return 'MSG:%s(%s)' % (self._msg_type, str(self._msg_data))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        # use the exclusve OR of our data (as suggested here: http://docs.python.org/2/reference/datamodel.html#object.__hash__ )
        _hash = hash(self._msg_type)
        for key, value in self._msg_data.items():   # dicts are unhashable, so we have to iterate thru... :(
            _hash = _hash ^ hash(key) ^ hash(value)

        return _hash

    def encode(self):
        ' return an encoded version of this Msg that can be sent/received. '
        return pickle.dumps(self)

    @staticmethod
    def decode(encoded_msg):
        ' create a Msg object from an encoded version of a Msg '
        return pickle.loads(encoded_msg)
