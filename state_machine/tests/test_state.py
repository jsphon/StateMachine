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

    def test_add_transition_to(self):
        s1 = State(name='s1')
        s2 = State(name='s2')
        c  = Condition()
        s1.add_transition_to(s2, c)

        self.assertEqual( s2, s1.listeners[c.listens_for][0].target )

    def test_find_next_triggered_transition(self):
        s = State(name='test state')

        s2 = State(name='s2')
        s3 = State(name='s3')

        s.add_transition_to( s2, ALWAYS_FALSE )
        s.add_transition_to( s3, ALWAYS_TRUE )

        model  = Model('test')
        data   = { ALWAYS_TRUE.listens_for:'hello' }
        result = s.find_next_triggered_transition( data, model )

        self.assertEqual(s3, result.target )

    def test_add_default_transition_to(self):

        s = State(name='test state')

        s2 = State(name='should get here')
        s3 = State(name='should not get here')

        s.add_transition_to(s3, ALWAYS_FALSE)
        s.add_default_transition_to(s2)

        model  = Model('test')
        data   = { ALWAYS_TRUE.listens_for:'hello' }
        t      = s.find_next_triggered_transition(data, model)

        self.assertEqual(s2, t.target)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
