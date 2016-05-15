'''
A simple Event Driven Finite State Machine class

'''

from state_machine.events import Observable, Observer
from state_machine.exception import StateMachineException
from state_machine.state import State, PseudoState
import traceback
from state_machine.data import Data

VERBOSE = True

CURRENT_STATE_NAME         = 'current_state_name'
CURRENT_STATE_COMMENT      = 'current_state_comment'
CURRENT_STATE_INPUT        = 'current_state_input'
CURRENT_STATE_START_RESULT = 'current_state_start_result'


class StateMachine( Observable ):

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

    @property
    def vars(self):
        return self._vars

    def reset(self):
        self.set_state(self.initial_state)

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

    @property
    def start_state(self):
        return self.initial_state
    
    def set_start_state(self, start_state):
        self.initial_state = start_state

    def notify(self, event):
        try:
            self._notify(event)
        except Exception as e:
            msg = 'Failed to run state %s\n'%self._current_state
            msg += traceback.format_exc()
            self.logger.error( msg )

    def _notify(self, event):

        if self._current_state:
            self._current_state.run(event)
            transition = self._current_state.next_transition(event)
            if transition:
                self._current_state.end(event)

                self.logger.info( 'Starting state %s', transition.target.name )

                self.set_state(transition.target)

                transition.target.start(event)

                if isinstance(transition.target, PseudoState):
                    self.logger.info('Target is a PseudoState')
                    self.notify(event)

        else:
            msg = 'State Machine has no current state'
            self.logger.error( msg )
            raise StateMachineException( msg )

    def set_state(self, state ):
        kwargs = {
            CURRENT_STATE_NAME: state.name,
            CURRENT_STATE_COMMENT:'',
        }
        self.data.set_multi( **kwargs )
        self._current_state = state
