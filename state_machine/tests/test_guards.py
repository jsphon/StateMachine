import unittest
import state_machine.guards as guards
from state_machine import FinalState, StateMachine, Event, CompositeState
import datetime

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

    def test_tick_before(self):
        dt = datetime.datetime.utcnow()
        dtp1 = dt+datetime.timedelta(1)
        dtm1 = dt-datetime.timedelta(1)

        state = None

        g = guards.tick_before(dt)

        e = Event('tick',dtp1)
        r = g(e, state)
        self.assertFalse(r)

        e = Event('tick',dtm1)
        r=g(e, state)
        self.assertTrue(r)

    def test_tick_after(self):

        dt = datetime.datetime.utcnow()
        dtp1 = dt+datetime.timedelta(1)
        dtm1 = dt-datetime.timedelta(1)

        state = None

        g = guards.tick_after(dt)

        e = Event('tick', dtp1)
        r = g(e, state)
        self.assertTrue(r)

        e = Event('tick', dtm1)
        r=g(e, state)
        self.assertFalse(r)
