import datetime
from state_machine import StateMachine, FinalState
import state_machine.guards as guards


class FixedDurationMachine(StateMachine):
    ''' A state machine that runs until a certain time
    '''
    def __init__(self, seconds=86400):
        super(FixedDurationMachine, self).__init__()

        self.date_threshold = datetime.datetime.utcnow()+datetime.timedelta(seconds=86400)

        state_tick = self.create_state('tick')
        state_final = self.create_state('final', FinalState)

        self.initial_state=state_tick
        state_tick.add_transition_to(state_tick, 'tick', guard=guards.tick_before(self.date_threshold), action=self.call_on_tick)
        state_tick.add_transition_to(state_final, 'tick', guard=guards.tick_after(self.date_threshold))

        self.tick_transition = state_tick.transitions[0]

    def call_on_tick(self, state, event):
        self.on_tick(state, event)

    def on_tick(self, state, event):
        print( 'Default ontick')


if __name__=='__main__':
    m = FixedDurationMachine()