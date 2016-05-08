import unittest

import state_machine.condition as condition
import state_machine.event as event
from mock import MagicMock

class ConditionTests(unittest.TestCase):

    def test_ALWAYS_TRUE(self):
        evt = event.Event()
        result = condition.ALWAYS_TRUE.is_triggered(evt)
        self.assertTrue( result )

    def test_ALWAYS_FALSE(self):
        evt = event.Event()
        result = condition.ALWAYS_FALSE.is_triggered( evt )
        self.assertFalse( result )

    def test_CompositeOrCondition(self):
        evt = event.Event()

        cond = condition.CompositeOrCondition( ( condition.ALWAYS_FALSE, condition.ALWAYS_TRUE ) )
        self.assertTrue( cond.is_triggered( evt ) )

        cond = condition.CompositeOrCondition( ( condition.ALWAYS_TRUE, condition.ALWAYS_TRUE ) )
        self.assertTrue( cond.is_triggered( evt ) )

        cond = condition.CompositeOrCondition( ( condition.ALWAYS_FALSE, condition.ALWAYS_FALSE ) )
        self.assertFalse( cond.is_triggered( evt ) )

    def test_CompositeAndCondition(self):
        cond = condition.CompositeAndCondition( ( condition.ALWAYS_FALSE, condition.ALWAYS_TRUE ) )
        self.assertFalse( cond.is_triggered(event) )

        cond = condition.CompositeAndCondition( ( condition.ALWAYS_TRUE, condition.ALWAYS_FALSE ) )
        self.assertFalse( cond.is_triggered(event) )

        cond = condition.CompositeAndCondition( ( condition.ALWAYS_FALSE, condition.ALWAYS_FALSE ) )
        self.assertFalse( cond.is_triggered(event) )

        cond = condition.CompositeAndCondition( ( condition.ALWAYS_TRUE, condition.ALWAYS_TRUE ) )
        self.assertTrue( cond.is_triggered(event) )