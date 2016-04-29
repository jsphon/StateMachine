

from state_machine.exceptions import StateMachineException
from state_machine.transition import Transition

class State( object ):

    def __init__( self, name='' ):
        self.name=name
        self._transitions = []

    def __repr__(self):
        return 'State:%s'%self.name

    def add_transition(self, transition ):
        if transition.source!=self:
            raise StateMachineException( 'transition source is not this state' )
        self._transitions.append( transition )

    def add_transition_to(self, target, conditions):
        """
        :param target: A State
        :param conditions: An iterable of conditions
        """
        t = Transition( self, target, conditions )
        self._transitions.append(t)

    def start(self, data, model, state_input=None ):
        return self.on_start( data, model, state_input )

    def on_start(self, data, model, state_input ):
        """ child classes can optionally extend this """
        pass

    def end(self, data, model ):
        self.onEnd( data, model )

    def on_end(self, data, model ):
        """ child classes can optionally extend this """
        pass

    def run(self, data, model):
        """
        For doing something everytime the machine ticks, such as storing state
        """
        pass

    def find_next_triggered_transition(self, data, model ):
        """ Find the first triggered transition """
        for transition in self._transitions:
            model.logger.info( 'Testing %s',transition )
            is_triggered = transition.is_triggered(data, model)
            if is_triggered:
                model.logger.info( 'Transitioning from %s to %s'%(self,transition.target))
                return transition


class FinalState(State):

    def __init__(self, name=None):
        name = name or 'Final State'
        super(FinalState, self).__init__(name)

    def find_next_triggered_transition(self, data, model):
        """ This does nothing """
        pass