'''
Created on 24 May 2015

@author: jon
'''
import unittest

from state_machine.exception import StateMachineException
from state_machine import Model, Event, State, StateMachine
from state_machine.condition import ALWAYS_FALSE, ALWAYS_TRUE, Condition

from mock import MagicMock


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
        c  = Condition()
        s1.add_transition_to(s2, c)

        self.assertEqual( s2, s1.listeners[c.listens_for][0].target )

    def test_next_transition(self):

        m = StateMachine()
        s = m.create_state(name='test state')

        s2 = m.create_state(name='s2')
        s3 = m.create_state(name='s3')

        s.add_transition_to( s2, ALWAYS_FALSE )
        s.add_transition_to( s3, ALWAYS_TRUE )

        event  = Event()
        result = s.next_transition( event )

        self.assertEqual(s3, result.target )

    def test_add_default_transition_to(self):

        m = StateMachine()
        s = m.create_state(name='test state')

        s2 = m.create_state(name='should get here')
        s3 = m.create_state(name='should not get here')

        s.add_transition_to(s3, ALWAYS_FALSE)
        s.add_default_transition_to(s2)

        event  = Event()
        t      = s.next_transition(event)

        self.assertEqual(s2, t.target)

    def test_start_stores_event(self):

        m = StateMachine()
        s = m.create_state(name='test state')

        e = Event()
        s.start(e)

        self.assertEqual(e, s.start_event)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
