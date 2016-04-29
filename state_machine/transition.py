
class Transition( object ):

    def __init__( self, source_state, target_state, conditions ):
        self.source = source_state
        self.target = target_state

        if isinstance( conditions, ( list, tuple ) ):
            self.conditions = conditions
        else:
            self.conditions = ( conditions, )

    def __repr__(self):
        condition_description = self.condition_description()
        return 'Transition from %s to %s, %s'%(self.source,self.target,condition_description)

    def condition_description(self):
        names = ( condition.name for condition in self.conditions )
        return 'Conditions:(%s)'%( ','.join( names ) )

    def is_triggered(self, data, model, start_result=None ):
        for c in self.conditions:
            result = c.is_triggered( data, model )
            if result:
                return result
        return False