from state_machine import FinalState

def is_final_state(event, state):
    return isinstance(state, FinalState)