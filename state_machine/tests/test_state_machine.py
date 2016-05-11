
import unittest

from state_machine.state_machine import StateMachine
from state_machine.exception import StateMachineException
from state_machine.state import State
from state_machine.condition import ALWAYS_TRUE, ALWAYS_FALSE, AlwaysTrue
from state_machine.model import Model
from state_machine import Event
from mock import MagicMock


class StateMachineTests(unittest.TestCase):

    def test___init__(self):
        sm = StateMachine( 'test machine' )

    def test_add_state(self):

        state = MagicMock()
        state.name='test_state'

        sm = StateMachine( 'test machine' )
        sm.add_state( state )

        self.assertEqual( state, sm.states[ 'test_state' ] )

        with self.assertRaises( StateMachineException ):
            sm.add_state( state )

    def test_notify(self):
        sm = StateMachine( 'test machine' )
        sm.notify( Event() )

    def test_notify_simple(self):
        '''
        A simple example of using a state machine
        '''

        sm = StateMachine( 'state machine 1' )

        src = State( 'src' )
        tgt = State( 'tgt' )

        src.add_transition_to( tgt, ALWAYS_TRUE )

        sm.set_state(src)
        evt  = Event(ALWAYS_TRUE.listens_for)

        # TEST
        sm.notify(evt)

        # VERIFY
        self.assertEqual(tgt, sm.current_state)


    def test_notify_handles_start_result(self):
        # # Need to be able to check that if on_start returns an event, then we handle it as well
        # e.g.
        #     order a pizza
        #     get back a pizza order event
        #     handle the pizza order event

        state_wait = State( 'Wait State' )

        state_action = State('Action State')
        state_action.on_start = lambda event: Event(name='action',payload='hello')

        state_final = State('Final State')
        state_final.on_start = MagicMock()

        state_wait.add_default_transition_to(state_action)
        state_action.add_default_transition_to(state_final)

        sm = StateMachine( 'state machine 1' )
        sm.set_state(state_wait)

        evt = Event()
        sm.notify(evt)

        sm.logger.info( 'We are in state %s',sm.current_state)
        self.assertEqual( state_final, sm.current_state)
        self.assertEqual('action', state_final.on_start.call_args[0][0].name)
        self.assertEqual('hello', state_final.on_start.call_args[0][0].payload)

    def test_notify_splits_streams_correctly(self):

        src  = State('src')
        tgt1 = State('tgt1')
        tgt2 = State('tgt2')

        c1  = AlwaysTrue()
        c1.listens_for = 'stream1'

        c2 = AlwaysTrue()
        c2.listens_for = 'stream2'

        src.add_transition_to( tgt1, c1 )
        src.add_transition_to( tgt2, c2 )

        sm = StateMachine('test machine')

        # Test1
        sm.set_state(src)
        sm.notify(Event('stream1'))
        self.assertEqual(tgt1, sm.current_state)

        # Test2
        sm.set_state(src)
        sm.notify(Event('stream2'))
        self.assertEqual(tgt2, sm.current_state)

        # Test3
        sm.set_state(src)
        sm.notify(Event())
        self.assertEqual(src, sm.current_state)

    def test_create_state(self):

        sm        = StateMachine('test')
        new_state = sm.create_state('new state')

        self.assertIsInstance(new_state, State)
        self.assertEqual('new state', new_state.name)
        self.assertEqual(new_state, sm.states['new state'])

    def test_create_state_with_custom_class(self):

        class CustomStateClass(State):

            def __init__(self,name, arg0, arg1):
                super(CustomStateClass, self).__init__(name)
                self.arg0=arg0
                self.arg1=arg1

        sm        = StateMachine('test')
        new_state = sm.create_state('new state', CustomStateClass, 0, arg1=1)

        self.assertIsInstance(new_state, CustomStateClass)
        self.assertEqual('new state', new_state.name)
        self.assertEqual(0, new_state.arg0)
        self.assertEqual(1, new_state.arg1)
        self.assertEqual(new_state, sm.states['new state'])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
