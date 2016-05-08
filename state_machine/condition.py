
class Condition( object ):

    listens_for = None
    name = ''

    def __init__( self, name='Condition' ):
        self.name = name

    def is_triggered( self, event ):
        raise NotImplementedError()


class AlwaysTrue( Condition ):

    def __init__(self):
        super( AlwaysTrue, self ).__init__( 'True' )

    def is_triggered( self, event ):
        return True


class AlwaysFalse(Condition):

    def __init__(self):
        super( AlwaysFalse, self ).__init__( 'False' )

    def is_triggered(self, event):
        return False


class CompositeOrCondition( Condition ):
    def __init__(self,conditions):
        self.conditions = conditions
        self.name = 'OR(%s)' % ','.join( c.name for c in conditions )

    def is_triggered( self, event ):
        return any(c.is_triggered(event) for c in self.conditions)


class CompositeAndCondition( Condition ):

    def __init__(self,conditions):
        self.conditions = conditions
        self.name = 'AND(%s)' % ','.join( c.name for c in conditions )

    def is_triggered( self, event ):
        return all( c.is_triggered(event) for c in self.conditions)


ALWAYS_TRUE = AlwaysTrue()
ALWAYS_FALSE = AlwaysFalse()