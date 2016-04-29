import unittest
from state_machine.transition import Transition
from state_machine.constants import CURRENT_STATE_NAME, CURRENT_STATE_COMMENT, CURRENT_STATE_INPUT, CURRENT_STATE_START_RESULT
from mock import MagicMock

class TransitionTests(unittest.TestCase):

    def test__init__(self):
        source = MagicMock()
        target = MagicMock()
        conditions = []
        t = Transition( source, target, conditions )

    def test_is_triggered_true(self):
        source = MagicMock()
        target = MagicMock()
        cond   = MagicMock()
        cond.is_triggered.return_value = True
        conditions = [ cond ]
        t = Transition( source, target, conditions )
        self.assertTrue( t.is_triggered( None, None ) )

    def test_is_triggered_false(self):
        source = MagicMock()
        target = MagicMock()
        cond   = MagicMock( return_value=False )
        cond.is_triggered.return_value = False
        conditions = [ cond ]
        t = Transition( source, target, conditions )
        self.assertFalse( t.is_triggered( None, None ) )