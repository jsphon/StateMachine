
class Transition( object ):

    def __init__( self, source_state, target_state, condition ):
        self.source = source_state
        self.target = target_state
        self.condition = condition

    def __repr__(self):
        condition_description = self.condition_description()
        return 'Transition from %s to %s, %s'%(self.source,self.target,condition_description)

    def condition_description(self):
        return 'Condition:(%s)'%self.condition.name

    def is_triggered(self, data, model, start_result=None ):
        return self.condition.is_triggered(data, model)
