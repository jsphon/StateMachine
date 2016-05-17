


class Event(object):
    name=''
    payload={}

    def __init__(self, name=None, payload=None):
        self.name = name
        self.payload = payload or {}
        self.processed=False

    def __repr__(self):
        return '<Event name="%s", payload=%s>'%(self.name,str(self.payload))