'''
Created on 24 May 2015

@author: jon
'''
import unittest
from state_machine import Event, State, StateMachine, PseudoState, CompositeState, Transition, FinalState
from state_machine.state import BaseState
from mock import MagicMock

import logging
logging.basicConfig(level=logging.DEBUG)

class ExampleTests(unittest.TestCase):

    def test(self):
        chatbot = StateMachine('chatbot')
        active_state = chatbot.create_state('active', CompositeState)
        sleeping_state = chatbot.create_state('sleeping', State)

        chatbot.initial_state=active_state

        active_state.add_transition_to(sleeping_state, 'sunset')
        sleeping_state.add_transition_to(active_state, 'sunrise')

        happy_state = active_state.create_state('happy')
        sad_state = active_state.create_state('sad')

        happy_state.add_transition_to(sad_state, 'criticism')
        sad_state.add_transition_to(happy_state, 'praise')

        active_state.initial_state=happy_state
        active_state.reset()

        sunrise=Event('sunrise')
        sunset=Event('sunset')

        chatbot.reset()

        chatbot.notify(sunset)
        self.assertEqual(sleeping_state, chatbot.current_state)

        chatbot.notify(sunrise)
        self.assertEqual(active_state, chatbot.current_state)

        #chatbot.logger.info('2nd run')
        #chatbot.notify(sunset)
        #self.assertEqual(sleeping_state, chatbot.current_state)

        #chatbot.notify(sunset)
        #self.assertEqual(sleeping_state, chatbot.current_state)

        #chatbot.notify(sunrise)
        #self.assertEqual(active_state, chatbot.current_state)

class CompositeStateTests(unittest.TestCase):

    def test___init__(self):
        m  = StateMachine()
        cs = CompositeState('composite', m)
        self.assertIsInstance(cs, CompositeState)

    def test_create_state(self):
        m  = StateMachine()

        cs = CompositeState('composite', m)
        ss = cs.create_state('substate1')

        self.assertIsInstance(ss, State)

    def xtest_next_transition_when_has_child_only(self):
        m  = StateMachine()

        cs = m.create_state('composite', CompositeState)

        ss1 = cs.create_state('substate1')
        ss2 = cs.create_state('substate2')
        ss1.add_transition_to(ss2, 'tick')
        cs.initial_state=ss1
        cs.reset()

        e = Event('tick')
        t = cs.next_transition(e)

        self.assertIsInstance(t, Transition)
        self.assertEqual(ss2, t.target)

    def xtest_next_transition_when_has_parent_only(self):
        m  = StateMachine()

        cs = m.create_state('composite', CompositeState)
        tgt = m.create_state('tgt' )

        cs.initial_state = cs.create_state('substate1')
        cs.reset()
        cs.add_transition_to(tgt)

        e = Event()
        t = cs.next_transition(e)

        self.assertEqual(tgt, t.target)

    def test_notify_child(self):
        m  = StateMachine()

        composite_state = m.create_state('composite', CompositeState)
        target_state    = m.create_state('target')
        composite_state.add_transition_to(target_state, 'tick')

        substate_source = composite_state.create_state('substate1')
        substate_target = composite_state.create_state('substate2')
        substate_source.add_transition_to(substate_target, 'tick')

        substate_source.on_end = MagicMock()
        substate_target.on_start = MagicMock()

        composite_state.initial_state=substate_source
        composite_state.reset()

        m.initial_state=composite_state
        m.reset()

        # Test, expecting the composite state's machine to transition
        e = Event('tick')
        m.notify(e)

        # Verify
        self.assertEqual(composite_state, m.current_state)
        self.assertEqual(substate_target, composite_state.current_state)
        self.assertEqual(1, substate_source.on_end.call_count)
        self.assertEqual(1, substate_target.on_start.call_count)

    def test_notify_parent(self):
        m  = StateMachine()

        composite_state = m.create_state('composite', CompositeState)
        target_state    = m.create_state('target')
        composite_state.add_transition_to(target_state, 'parent tick')

        substate_source = composite_state.create_state('substate1')
        substate_target = composite_state.create_state('substate2')
        substate_source.add_transition_to(substate_target, 'tick')

        substate_source.on_end = MagicMock()
        substate_target.on_start = MagicMock()

        composite_state.initial_state=substate_source
        composite_state.reset()

        composite_state.on_end = MagicMock()
        target_state.on_start = MagicMock()

        m.initial_state=composite_state
        m.reset()

        # Test, expecting the composite state's machine to transition
        e = Event('parent tick')
        m.notify(e)

        # Verify
        self.assertEqual(target_state, m.current_state)
        self.assertIsInstance(composite_state.current_state, FinalState)

        self.assertEqual(1, substate_source.on_end.call_count)
        self.assertEqual(0, substate_target.on_start.call_count)

        self.assertEqual(1, composite_state.on_end.call_count)
        self.assertEqual(1, target_state.on_start.call_count)

    def test_notify_observers(self):
        """
        Test that a substate still notifies observers
        """
        # SETUP
        m  = StateMachine('Observed')
        composite_state = m.create_state('composite', CompositeState)
        sub_state = composite_state.create_state('substate')

        listener = StateMachine('Listener')
        listener.notify = MagicMock()

        m.register_observer('tick', listener)

        # TEST
        e = Event('tick')
        sub_state.notify_observers(e)
        m.flush()

        self.assertEqual(1, listener.notify.call_count)
        listener.notify.assert_called_with(e)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
