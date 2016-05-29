import unittest
import state_machine.guards as guards
from state_machine import FinalState, StateMachine, Event

class GuardTests(unittest.TestCase):

    def test_is_final_state(self):
        m=StateMachine()
        s=m.create_state('final', FinalState)
        e=Event()
        self.assertTrue( guards.is_final_state(e, s))

    def test_is_final_state_using_subclass(self):

        class AnotherFinalState(FinalState):
            pass

        m = StateMachine()
        s = m.create_state('final', AnotherFinalState)
        e = Event()
        self.assertTrue( guards.is_final_state(e, s) )

