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


def tick_before(dt):
    def inner_func(event, state):
        return event.payload<dt
    return inner_func


def tick_after(dt):
    def inner_func(event, state):
        return event.payload>dt
    return inner_func