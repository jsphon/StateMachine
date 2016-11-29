import unittest
from state_machine import Transition, Event
from unittest.mock import MagicMock
from state_machine.condition import ALWAYS_TRUE, ALWAYS_FALSE

class TransitionTests(unittest.TestCase):

    def test__init__(self):
        source = MagicMock()
        target = MagicMock()
        trigger = MagicMock()
        guard = MagicMock()
        action = MagicMock()

        t = Transition(source, target, trigger, guard, action)

        self.assertEqual(source, t.source)
        self.assertEqual(target, t.target)
        self.assertEqual(trigger, t.trigger)
        self.assertEqual(guard, t.guard)
        self.assertEqual(action, t.action)

    def test_is_triggered_true_without_trigger(self):
        current_state = MagicMock()
        source = MagicMock()
        target = MagicMock()
        event = MagicMock()
        t = Transition(source, target)

        r = t.is_triggered(event)

        self.assertTrue( r )

    def test_is_triggered_true_with_trigger(self):
        current_state = MagicMock()
        source = MagicMock()
        target = MagicMock()
        event = Event('test_event')
        t = Transition(source, target, trigger='test_event')

        r = t.is_triggered(event)

        self.assertTrue( r )

    def test_is_triggered_true_with_guard(self):

        current_state = MagicMock()
        source = MagicMock()
        target = MagicMock()
        event = MagicMock()
        guard = lambda event, current_state:True
        t = Transition(source, target, guard=guard)

        r = t.is_triggered(event)

        self.assertTrue( r )

    def test_is_triggered_false_with_guard(self):

        current_state = MagicMock()
        source = MagicMock()
        target = MagicMock()
        event = MagicMock()
        guard = lambda event, current_state:False
        t = Transition(source, target, guard=guard)

        r = t.is_triggered(event)

        self.assertFalse( r )
