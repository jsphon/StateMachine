
from state_machine.state import State, FinalState
from state_machine.state_machine import StateMachine

class CompositeState(State, StateMachine):

    def __init__(self, name, machine):
        State.__init__(self, name, machine)
        StateMachine.__init__(self, name)

    def run(self, event):
        State.run(self,event)
        self._current_state.run( event )

    def start(self, event):
        self.logger.info( 'Starting %s'%self.name)
        State.start(self, event)
        self.reset()

    def end(self, event):
        State.end(self,event)
        self._current_state.end(event)
        self.set_state(FinalState())
