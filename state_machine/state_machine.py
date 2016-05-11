'''
A simple Event Driven Finite State Machine class

'''

from state_machine.events import Observable, Observer
from state_machine.exception import StateMachineException
from state_machine.state import State
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
                        start_state = None,
                        data = None,
                        ):

        self.name           = name
        self._start_state   = None
        self.states         = {}

        self._current_state = None

        self.logger = logger
        if self.logger is None:
            import logging
            self.logger = logging.getLogger( 'default' )
            self.logger.setLevel( logging.INFO )

        self.data = data or Data( name )

    def create_state(self, name, StateClass=State, *args, **kwargs):
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
        return self._start_state
    
    def set_start_state(self, start_state):
        self._start_state = start_state

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
                #model.logger.info( 'Leaving state %s for %s'%(model.current_state.name, transition.target.name))
                self._current_state.end(event)

                self.logger.info( 'Starting state %s', transition.target.name )
                #model.logger.info( 'input data: %s', str( transition ) )

                target_start_event = transition.target.start(event)

                self.logger.info( '%s started successfully with result: %s',transition.target.name,target_start_event)
                #model.logger.info( 'Updating persistent state data')

                self.set_state(transition.target)

                if target_start_event:
                    self.notify(target_start_event)

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




#
# Pondering how to get info to condition in elegant manner
'''

    Order Placed Event
    State receives order placed event
    State listens for order to be filled

    How about:
        When state starts listening, it modifies the condition to listen for the order id
        When the state ends, set the order id to None (for safety, not necessary)

    Pros:
        Involves sending less data to transition/condition
        Will keep the conditions cleaner.
        Can probably build a chart out of this

    Cons:
        A little more complexity in state
        Will need to keep track of the transition/condition in state


'''
