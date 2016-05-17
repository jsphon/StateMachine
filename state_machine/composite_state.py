
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
        State.start(event)
        self.reset()

    def end(self, event):
        State.end(self,event)
        self.set_state(FinalState())

    def notify_observers(self, event):
        StateMachine.notify_observers(self, event)
