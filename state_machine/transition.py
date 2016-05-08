
class Transition( object ):

    def __init__( self, target_state, condition ):
        self.target = target_state
        self.condition = condition

    def __repr__(self):
        condition_description = self.condition_description()
        return 'Transition from to %s, %s'%(self.target,condition_description)

    def condition_description(self):
        return 'Condition:(%s)'%self.condition.name

    def is_triggered(self, event):
        return self.condition.is_triggered(event)
