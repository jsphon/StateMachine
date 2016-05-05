import unittest
from state_machine.transition import Transition
from state_machine.constants import CURRENT_STATE_NAME, CURRENT_STATE_COMMENT, CURRENT_STATE_INPUT, CURRENT_STATE_START_RESULT
from mock import MagicMock
from state_machine.condition import ALWAYS_TRUE, ALWAYS_FALSE

class TransitionTests(unittest.TestCase):

    def test__init__(self):
        source = MagicMock()
        target = MagicMock()
        conditions = []
        t = Transition( source, target, conditions )

    def test_is_triggered_true(self):
        source = MagicMock()
        target = MagicMock()
        t = Transition( source, target, ALWAYS_TRUE )
        self.assertTrue( t.is_triggered( None, None ) )

    def test_is_triggered_false(self):
        source = MagicMock()
        target = MagicMock()
        t = Transition( source, target, ALWAYS_FALSE )
        self.assertFalse( t.is_triggered( None, None ) )