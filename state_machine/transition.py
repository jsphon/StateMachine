
class Transition( object ):

    def __init__( self, source_state, target_state, trigger=None, guard=None, action=None ):
        self.source = source_state
        self.target = target_state
        self.trigger = trigger
        self.guard = guard
        self.action = action

    def __repr__(self):
        return 'Transition from %s to %s'%(self.source,self.target)

    def is_triggered(self, event):

        if self.trigger and event.name!=self.trigger:
            return False

        if self.guard:
            return self.guard(event, self.source)

        return True


class DefaultTransition(Transition):

    def __init__(self, target_state):
        self.target = target_state
        self.condition = None

    def __repr__(self):
        return 'Default Transition to %s'%self.target

    def is_triggered(self, event):
        return True