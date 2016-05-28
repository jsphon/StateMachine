
class Transition( object ):

    def __init__( self, source_state, target_state, trigger=None, guard=None, action=None ):
        self.source = source_state
        self.target = target_state
        self.trigger = trigger
        self.guard = guard
        self.action = action

    def __repr__(self):
        return 'Transition from %s to %s'%(self.source,self.target)

    def to_str(self):
        trigger = self.trigger if self.trigger else ''
        guard = '[%s]'%self.guard.__name__ if self.guard else ''
        action = '/%s'%self.action.__name__ if self.action else ''
        return '%s%s%s'%(trigger, guard, action)

    def is_triggered(self, event):

        if self.trigger and event.name!=self.trigger:
            return False

        if self.guard:
            return self.guard(event, self.source)

        return True


class DefaultTransition(Transition):

    def __init__(self, source_state, target_state):
        super(DefaultTransition, self).__init__(source_state, target_state)

    def __repr__(self):
        return 'Default Transition from %s to %s'%(self.source,self.target)
