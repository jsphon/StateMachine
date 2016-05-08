import unittest
from state_machine import Transition, Event
from mock import MagicMock
from state_machine.condition import ALWAYS_TRUE, ALWAYS_FALSE

class TransitionTests(unittest.TestCase):

    def test__init__(self):
        target = MagicMock()
        conditions = []
        t = Transition(target, conditions)

    def test_is_triggered_true(self):
        target = MagicMock()
        t = Transition(target, ALWAYS_TRUE)
        self.assertTrue( t.is_triggered(Event()) )

    def test_is_triggered_false(self):
        target = MagicMock()
        t = Transition(target, ALWAYS_FALSE)
        self.assertFalse( t.is_triggered(Event()) )