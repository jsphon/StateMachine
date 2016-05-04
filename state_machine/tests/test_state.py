'''
Created on 24 May 2015

@author: jon
'''
import unittest

from state_machine.exception import StateMachineException
from state_machine.state import State
from state_machine import Model
from state_machine.transition import Transition
from state_machine.condition import ALWAYS_FALSE, ALWAYS_TRUE, Condition

from mock import MagicMock


class StateTests(unittest.TestCase):

    def test___init__(self):
        s = State(name='test state')

    def test_add_transition(self):
        s = State(name='test state')
        t = MagicMock()
        t.source = s
        s.add_transition( t )
        self.assertEqual( t, s._transitions[0] )

    def test_add_transition_exception(self):
        s = State(name='test state')
        t = MagicMock()

        with self.assertRaises( StateMachineException ):
            s.add_transition( t )

    def test_add_transition_to(self):
        s1 = State(name='s1')
        s2 = State(name='s2')
        c  = Condition()
        s1.add_transition_to(s2, c)

        self.assertEqual( s2, s1._transitions[0].target )

    def test_find_next_triggered_transition(self):
        s = State(name='test state')

        s2 = State(name='s2')
        s3 = State(name='s3')

        s.add_transition_to( s2, ALWAYS_FALSE )
        s.add_transition_to( s3, ALWAYS_TRUE )

        model = MagicMock()
        result = s.find_next_triggered_transition( None, model )

        self.assertEqual( 2, len( s._transitions ) )
        self.assertEqual(s._transitions[1], result )

    def test_add_default_transition_to(self):

        s = State(name='test state')

        s2 = State(name='should get here')
        s3 = State(name='should not get here')

        s.add_transition_to(s3, ALWAYS_FALSE)
        s.add_default_transition_to(s2)

        model  = MagicMock()
        t      = s.find_next_triggered_transition(None,model)

        self.assertEqual(s2, t.target)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
