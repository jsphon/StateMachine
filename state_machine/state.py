

from state_machine.exception import StateMachineException
from state_machine.transition import Transition
from collections import defaultdict

class State( object ):

    def __init__( self, name='', default_transition=None ):
        self.name=name
        #self._transitions = []
        self.default_transition = None
        self.listeners = defaultdict(list)

    def __repr__(self):
        return 'State:%s'%self.name

    def add_default_transition_to(self, target):
        """
        Add a default transition to target
        :param target:  the target state
        :return:
        """
        self.default_transition = Transition(self, target, None)

    def add_transition_to(self, target, condition):
        """
        :param target: A State
        :param condition: A condition
        """
        t = Transition( self, target, condition )
        self.listeners[condition.listens_for].append(t)

    def start(self, data, model):#, state_input=None ):
        return self.on_start( data, model)#, state_input )

    def on_start(self, data, model):#, state_input=None ):
        """ child classes can optionally extend this """
        pass

    def end(self, data, model ):
        self.on_end( data, model )

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

        if data:

            for data_stream, payload in data.items():
                model.logger.info( '%s, %s', data_stream, payload)
                transitions = self.listeners[data_stream]
                model.logger.info( 'We have %i transitions'%len(transitions))
                for t in transitions:
                    model.logger.info('Testing transition %s',t)
                    if t.is_triggered(payload, model):
                        model.logger.info( 'Returning %s',t)
                        return t

        return self.default_transition


class FinalState(State):

    def __init__(self, name=None):
        name = name or 'Final State'
        super(FinalState, self).__init__(name)

    def find_next_triggered_transition(self, data, model):
        """ This does nothing """
        pass