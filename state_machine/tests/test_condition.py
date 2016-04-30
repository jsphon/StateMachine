import unittest

import state_machine.condition as condition
from mock import MagicMock

class ConditionTests(unittest.TestCase):

    def test_ALWAYS_TRUE(self):

        result = condition.ALWAYS_TRUE.is_triggered( None, None )
        self.assertTrue( result )

    def test_ALWAYS_FALSE(self):
        result = condition.ALWAYS_FALSE.is_triggered( None, None )
        self.assertFalse( result )

    def test_CompositeOrCondition(self):
        cond = condition.CompositeOrCondition( ( condition.ALWAYS_FALSE, condition.ALWAYS_TRUE ) )
        self.assertTrue( cond.is_triggered( None, None ) )

        cond = condition.CompositeOrCondition( ( condition.ALWAYS_TRUE, condition.ALWAYS_TRUE ) )
        self.assertTrue( cond.is_triggered( None, None ) )

        cond = condition.CompositeOrCondition( ( condition.ALWAYS_FALSE, condition.ALWAYS_FALSE ) )
        self.assertFalse( cond.is_triggered( None, None ) )

    def test_CompositeAndCondition(self):
        cond = condition.CompositeAndCondition( ( condition.ALWAYS_FALSE, condition.ALWAYS_TRUE ) )
        self.assertFalse( cond.is_triggered( None, None ) )

        cond = condition.CompositeAndCondition( ( condition.ALWAYS_TRUE, condition.ALWAYS_FALSE ) )
        self.assertFalse( cond.is_triggered( None, None ) )

        cond = condition.CompositeAndCondition( ( condition.ALWAYS_FALSE, condition.ALWAYS_FALSE ) )
        self.assertFalse( cond.is_triggered( None, None ) )

        cond = condition.CompositeAndCondition( ( condition.ALWAYS_TRUE, condition.ALWAYS_TRUE ) )
        self.assertTrue( cond.is_triggered( None, None ) )