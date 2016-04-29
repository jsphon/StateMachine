'''
A simple Finite State Machine class

'''

from datetime import datetime
from state_machine.exception import StateMachineException
import json
import os
import traceback

VERBOSE = True

CURRENT_STATE_NAME         = 'current_state_name'
CURRENT_STATE_COMMENT      = 'current_state_comment'
CURRENT_STATE_INPUT        = 'current_state_input'
CURRENT_STATE_START_RESULT = 'current_state_start_result'


class StateMachine( object ):

    def __init__( self, name='' ):

        self.name           = name 
        self._default_state = None
        self.states         = {}

    def add_state(self,new_state):
        if new_state.name in self.states:
            raise StateMachineException( 'State %s Already Exists'%new_state.name )
        else:
            self.states[ new_state.name ] = new_state            
            
    @property
    def default_state(self):
        return self._default_state
    
    def set_default_state(self, default_state):
        self._default_state = default_state
         
    def run(self, data, model):
        try:
            self._run( data, model )
        except Exception as e:
            msg = 'Failed to run state %s\n'%model.current_state
            msg += traceback.format_exc()
            model.logger.error( msg )
        
    def _run(self, data, model ):
        
        if model.current_state:
            model.current_state.run( data, model )
            transition = model.current_state.find_next_triggered_transition( data, model )
            if transition:
                #model.logger.info( 'Leaving state %s for %s'%(model.current_state.name, transition.target.name))
                model.current_state.end( data, model )

                #model.logger.info( 'Starting state %s', transition.target.name )
                #model.logger.info( 'input data: %s', str( transition ) )
                
                start_result = transition.target.start( data, model )

                #model.logger.info( '%s started successfully with result: %s',transition_state.target.name,str(start_result))
                #model.logger.info( 'Updating persistent state data')

                model.set_state( transition.target, start_result )

                self.run( data, model, start_result )

        else:
            msg = 'Model has no current state'
            model.logger.error( msg )
            raise StateMachineException( msg )        