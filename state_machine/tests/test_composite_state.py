import unittest
from state_machine import Event, State, StateMachine, CompositeState, FinalState
from mock import MagicMock

import logging
logging.basicConfig(level=logging.DEBUG)


class ExampleTests(unittest.TestCase):

    def setUp(self):

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

        chatbot.reset()

        self.chatbot = chatbot
        self.active_state = active_state
        self.sleeping_state = sleeping_state
        self.happy_state = happy_state
        self.sad_state = sad_state

        self.sunrise=Event('sunrise')
        self.sunset=Event('sunset')

        self.criticism=Event('criticism')
        self.praise=Event('praise')

    def test_parent(self):
        '''
        Test interactions on the parent only
        '''
        for _ in range(100):
            self.chatbot.notify(self.sunset)
            self.assertEqual(self.sleeping_state, self.chatbot.current_state)

            self.chatbot.notify(self.sunrise)
            self.assertEqual(self.active_state, self.chatbot.current_state)
            self.assertEqual(self.happy_state, self.chatbot.current_state.current_state)

    def test_child(self):
        '''
        Test interactions on the child only
        '''

        self.chatbot.notify(self.criticism)
        self.assertEqual(self.active_state, self.chatbot.current_state)
        self.assertEqual(self.sad_state, self.active_state.current_state)

        self.chatbot.notify(self.praise)
        self.assertEqual(self.active_state, self.chatbot.current_state)
        self.assertEqual(self.happy_state, self.active_state.current_state)

    def test_both(self):
        '''
        Test interactions on both parent and child
        '''
        for _ in range(100):
            self.chatbot.notify(self.sunset)
            self.assertEqual(self.sleeping_state, self.chatbot.current_state)

            self.chatbot.notify(self.criticism)
            self.assertEqual(self.sleeping_state, self.chatbot.current_state)

            self.chatbot.notify(self.praise)
            self.assertEqual(self.sleeping_state, self.chatbot.current_state)

            self.chatbot.notify(self.sunrise)
            self.assertEqual(self.active_state, self.chatbot.current_state)
            self.assertEqual(self.happy_state, self.chatbot.current_state.current_state)

            self.chatbot.notify(self.criticism)
            self.assertEqual(self.active_state, self.chatbot.current_state)
            self.assertEqual(self.sad_state, self.chatbot.current_state.current_state)


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
