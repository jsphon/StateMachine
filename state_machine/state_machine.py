'''
A simple Event Driven Finite State Machine class

'''

from state_machine.events import DelayedObservable
from state_machine.exception import StateMachineException
from state_machine.state import State, PseudoState, FinalState
#from state_machine.composite_state import CompositeState
import traceback
from state_machine.data import Data

VERBOSE = True

CURRENT_STATE_NAME         = 'current_state_name'
CURRENT_STATE_COMMENT      = 'current_state_comment'
CURRENT_STATE_INPUT        = 'current_state_input'
CURRENT_STATE_START_RESULT = 'current_state_start_result'


class StateMachine(DelayedObservable):

    def __init__(self, name='',
                        logger=None,
                        initial_state = None,
                        data = None,
                        ):

        super(StateMachine,self).__init__()

        self.name           = name
        self.initial_state   = initial_state
        self.states         = {}

        self._current_state = None

        self.logger = logger
        if self.logger is None:
            import logging
            self.logger = logging.getLogger( 'default' )
            self.logger.setLevel( logging.INFO )

        self.data = data or Data( name )
        self._vars = {}

    def __repr__(self):
        return '<StateMachine name="%s">'%self.name

    @property
    def vars(self):
        return self._vars

    def initialise(self):
        self.set_state(self.initial_state)
        if issubclass( type(self.initial_state), StateMachine):
            self._current_state.initialise()

    def create_state(self, name, StateClass=None, *args, **kwargs):
        StateClass = StateClass or State
        self.logger.info('Creating state of type %s',StateClass)
        new_state = StateClass(name, self, *args, **kwargs)
        self.add_state(new_state)
        return new_state

    def add_state(self,new_state):
        if new_state.name in self.states:
            raise StateMachineException( 'State %s Already Exists'%new_state.name )
        else:
            self.states[ new_state.name ] = new_state            

    @property
    def current_state(self):
        return self._current_state

    def notify(self, event):

        self._current_state.run(event)

        if issubclass( type(self._current_state), StateMachine):
            child_machine = self._current_state
            child_transition = child_machine._current_state.next_transition(event)
            if child_transition:
                child_machine.process_transition(child_transition, event)
            else:
                self.process_event(event)
        else:
            self.process_event(event)

        self.flush()

    def process_event(self, event):
        transition = self._current_state.next_transition(event)
        if transition:
            self.process_transition(transition, event)

    def process_transition(self, transition, event):
        self._current_state.end(event)
        self.logger.info( '%s transitioning to state %s', self.name, transition.target)
        if transition.target!=self.current_state:
            # This is a self transition, so do no call set_state
            self.set_state(transition.target)
        if transition.action:
            transition.action(event, self._current_state)
        transition.target.start(event)
        if isinstance(transition.target, PseudoState):
            # Pseudo states are for making choices/decisions.
            # Send the event to the target to see what decision it makes

            # We can call proces_event instead of notify, as at time of writing,
            # we don't need the other logic contained in notify
            self.process_event(event)
            #self.notify(event)

    def set_state(self, state ):
        kwargs = {
            CURRENT_STATE_NAME: state.name,
            CURRENT_STATE_COMMENT:'',
        }
        self.data.set_multi( **kwargs )
        self._current_state = state
