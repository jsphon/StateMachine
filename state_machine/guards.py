from state_machine import FinalState

def is_final_state(event, state):
    return isinstance(state, FinalState)


def is_child_final(event, state):
    """

    :param event:
    :param state: Composite State
    :return: True if state's child is Final
    """
    return isinstance(state.current_state, FinalState)