


class Event(object):
    name=''
    payload={}

    def __init__(self, name=None, payload=None):
        self.name = name
        self.payload = payload or {}