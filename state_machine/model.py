from collections import defaultdict
from state_machine.constants import CURRENT_STATE_NAME, CURRENT_STATE_COMMENT, CURRENT_STATE_INPUT, CURRENT_STATE_START_RESULT
from state_machine.data import Data


class Model( object ):
    """ For storing state machine data """

    def __init__(self, name, logger=None, data=None, state_machine=None):

        self.name = name
        self.state_machine = state_machine
        self._current_state  = None
        self._current_state_input = None
        self._current_state_start_result = None

        self.logger         = logger
        if self.logger is None:
            import logging
            self.logger = logging.getLogger( 'default' )
            self.logger.setLevel( logging.INFO )

        self.listeners = defaultdict(set)

        self.data = data or Data( name )

    def add_listener(self, listener, event_name):
        self.listeners[event_name].add( listener )

    def send_event(self, event_name, data):
        event_listeners = self.listeners[event_name]
        for l in event_listeners:
            l.state_machine.run(data,l)

    def recover_state(self, machine):
        """ Recover the state of the machine """
        state_name = self.load_state_name()
        if state_name:
            self._current_state = machine.states[ state_name ]
        else:
            self.logger.info( 'No state to recover, so setting to %s', self._default_state.name )
            self.set_state( self._default_state )
            self._current_state = self._default_state

    def load_state_name(self):
        return self.data.get( CURRENT_STATE_NAME )

    def set_state(self, state, state_input=None, start_result=None ):
        kwargs = {
            CURRENT_STATE_NAME: state.name,
            CURRENT_STATE_INPUT: state_input,
            CURRENT_STATE_START_RESULT: start_result,
            CURRENT_STATE_COMMENT:'',
        }
        self.data.set_multi( **kwargs )
        self._current_state = state
        self._current_state_input = state_input
        self._current_state_start_result = start_result

    def set_state_comment(self, comment ):
        self.data.set( CURRENT_STATE_COMMENT, comment )

    @property
    def current_state(self):
        return self._current_state

    @property
    def current_state_input(self):
        """ Return the input data for the current state
        """
        return self._current_state_input

    @property
    def current_state_start_result(self):
        """ Return the result of onStart """
        return self._current_state_start_result