import unittest
import state_machine.guards as guards
from state_machine import FinalState, StateMachine, Event, CompositeState

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

    def test_is_child_final_true(self):
        m=StateMachine()
        s=m.create_state('final', CompositeState)
        f=s.create_state('sfinal', FinalState)
        s.set_state(f)
        e=Event()
        self.assertTrue( guards.is_child_final(e, s))

    def test_is_child_final_false(self):
        m=StateMachine()
        s=m.create_state('final', CompositeState)
        c=s.create_state('s')
        s.set_state(c)
        e=Event()
        self.assertFalse( guards.is_child_final(e, s))

