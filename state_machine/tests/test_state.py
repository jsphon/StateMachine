'''
Created on 24 May 2015

@author: jon
'''
import unittest
from state_machine import Event, State, StateMachine, PseudoState
from state_machine.state import BaseState
from mock import MagicMock

class BaseStateTests(unittest.TestCase):

    def test___init__(self):
        m = StateMachine()
        bs = BaseState( 'name', m)
        self.assertIsInstance(bs, BaseState)

    def test_on_start(self):

        # SETUP
        m = StateMachine()
        bs = BaseState( 'name', m)
        bs.on_start = MagicMock()

        #TEST
        e = Event()
        bs.start(e)

        #VERIFY
        bs.on_start.assert_called_once_with(e, bs)

    def test_on_end(self):

        # SETUp
        m = StateMachine()
        bs = BaseState( 'name', m)
        bs.on_end = MagicMock()

        #TEST
        e = Event()
        bs.end(e)

        #VERIFY
        bs.on_end.assert_called_once_with(e, bs)






class PseudoStateTests(unittest.TestCase):

    def test___init__(self):

        m = StateMachine()
        s = PseudoState('ps', m)
        self.assertIsInstance(s, PseudoState)

    def test_add_transition_to(self):
        m   = StateMachine()
        ps  = m.create_state('ps', PseudoState)
        tgt1 = m.create_state('tgt1')

        g1 = lambda event, state: True
        ps.add_transition_to(tgt1, guard=g1)

        self.assertEqual(1, len(ps.transitions))
        self.assertEqual(tgt1, ps.transitions[0].target)

    def test_next_transition(self):

        m   = StateMachine()
        ps  = m.create_state('ps', PseudoState)
        tgt1 = m.create_state('tgt1')
        tgt2 = m.create_state('tgt2')

        g1 = lambda event, state: True
        ps.add_transition_to(tgt1, guard=g1)

        g2 = lambda event, state: False
        ps.add_transition_to(tgt2, guard=g2)

        e = Event()
        t = ps.next_transition(e)
        self.assertEqual(tgt1, t.target)


class StateTests(unittest.TestCase):

    def test___init__(self):
        m = StateMachine()
        s = State('test state', m)

        self.assertEqual('test state', s.name)
        self.assertEqual(m, s.machine)

    def test_notify_observers(self):
        m = StateMachine()
        m.notify_observers = MagicMock()
        s = State('test state', m)

        e = Event()
        s.notify_observers(e)

        self.assertEqual(1, m.notify_observers.call_count)
        self.assertEqual(e, m.notify_observers.call_args[0][0])

    def test_add_transition_to(self):
        m  = StateMachine()
        s1 = m.create_state(name='s1')
        s2 = m.create_state(name='s2')

        s1.add_transition_to(s2, 'test event...')

        self.assertEqual( s2, s1.transitions_by_trigger['test event...'][0].target )

    def test_add_transition_to_without_params(self):
        m  = StateMachine()
        m.logger.info(m.states)
        s1 = m.create_state(name='s1')
        s2 = m.create_state(name='s2')

        s1.add_transition_to(s2)

        self.assertEqual( 0, len( s1.transitions_by_trigger ) )
        self.assertEqual( s2, s1.default_transition.target )

    def test_next_transition(self):

        m = StateMachine()
        s = m.create_state(name='test state')

        s2 = m.create_state(name='s2')
        s3 = m.create_state(name='s3')

        s.add_transition_to( s2, 'ignore' )
        s.add_transition_to( s3, 'trigger' )

        event  = Event('trigger')
        result = s.next_transition( event )

        self.assertEqual(s3, result.target )

    def test_transition_to_default(self):

        m = StateMachine()
        s = m.create_state(name='test state')

        s2 = m.create_state(name='should get here')
        s3 = m.create_state(name='should not get here')

        s.add_transition_to(s3, 'test event')
        s.add_transition_to(s2)

        event  = Event('any event')
        t      = s.next_transition(event)

        self.assertEqual(s2, t.target)

    def test_start_stores_event(self):

        m = StateMachine()
        s = m.create_state(name='test state')

        e = Event()
        s.start(e)

        self.assertEqual(e, s.start_event)

    def test_transitions(self):

        m = StateMachine()
        s = m.create_state(name='test state')

        s2 = m.create_state(name='s2')
        s3 = m.create_state(name='s3')

        s.add_transition_to( s2, 'ignore' )
        s.add_transition_to( s3, 'trigger' )

        transitions = s.transitions

        self.assertIsInstance( transitions, list )
        self.assertEqual(2, len( transitions ))

    def test_to_str(self):

        m = StateMachine()
        s = m.create_state(name='test state')

        s2 = m.create_state(name='s2')
        s.add_transition_to( s2, 'trigger' )

        r = s.transitions[0].to_str()

        self.assertEqual('trigger', r)

    def test_to_str2(self):

        def guard_fn(event, state):
            return True

        def action_fn(event, state):
            pass

        m = StateMachine()
        s = m.create_state(name='test state')

        s2 = m.create_state(name='s2')
        s.add_transition_to( s2, 'trigger', guard=guard_fn, action=action_fn )

        r = s.transitions[0].to_str()

        self.assertEqual('trigger[guard_fn]/action_fn', r)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
