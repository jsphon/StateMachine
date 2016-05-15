
class Transition( object ):

    def __init__( self, source_state, target_state, trigger=None, guard=None, action=None ):
        self.source = source_state
        self.target = target_state
        self.trigger = trigger
        self.guard = guard
        self.action = action

    def __repr__(self):
        condition_description = self.condition_description()
        return 'Transition to %s, %s'%(self.target,condition_description)

    def condition_description(self):
        return 'Condition:(%s)'%self.condition.name

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