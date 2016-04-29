
class Condition( object ):

    def __init__( self, name='Condition' ):
        self.name = name

    def is_triggered( self, data, model ):
        raise NotImplementedError()

class AlwaysTrue( Condition ):

    def __init__(self):
        super( AlwaysTrue, self ).__init__( 'True' )

    def is_triggered( self, data, model ):
        return True

class AlwaysFalse(Condition):

    def __init__(self):
        super( AlwaysFalse, self ).__init__( 'False' )

    def is_triggered( self, data, model ):
        return False

class CompositeOrCondition( Condition ):
    def __init__(self,conditions):
        self.conditions = conditions
        self.name = 'OR(%s)' % ','.join( c.name for c in conditions )

    def is_triggered( self, data, model ):
        for c in self.conditions:
            r,msg = c.is_triggered( data, model )
            if r:
                return r, msg
        return False, None


class CompositeAndCondition( Condition ):

    def __init__(self,conditions):
        self.conditions = conditions
        self.name = 'AND(%s)' % ','.join( c.name for c in conditions )

    def is_triggered( self, data, model ):
        for c in self.conditions:
            r,msg = c.is_triggered( data, model )
            if not r:
                return r, msg
        return r, msg


class OppositeCondition( Condition ):
    """ Return the inverse of Condition """

    def __init__(self, source):
        self.name = 'NOT(%s)'%source.name
        self.source=source

    def is_triggered(self, data, model):
        r, _ = self.source.is_triggered( data, model )
        return not r, None