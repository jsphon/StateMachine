
import unittest

from state_machine.state_machine import StateMachine
from state_machine.exception import StateMachineException
from state_machine.state import State
from state_machine.condition import AlwaysTrue, AlwaysFalse
from state_machine.model import Model
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

    def test_run(self):
        data  = None
        model = MagicMock()
        sm = StateMachine( 'test machine' )
        sm._run = MagicMock()
        sm.run( data, model )

    def test_run_logs_exception(self):
        data  = None
        model = MagicMock()
        sm = StateMachine( 'test machine' )
        sm._run = MagicMock( side_effect=StateMachineException( 'intentional' ) )

        sm.run( data, model )

        self.assertEqual( 1, model.logger.error.call_count )

    def test_run_without_current_state(self):
        sm = StateMachine( 'state machine 1' )
        model = MagicMock()
        model.current_state = None

        with self.assertRaises( StateMachineException ) as e:
            sm._run(None, model)
        self.assertEqual( 'Model has no current state', e.exception.msg )

    def test_run_simple(self):
        '''
        A simple test from state1 to state2
        '''

        sm = StateMachine( 'state machine 1' )

        src = State( 'src' )
        tgt = State( 'tgt' )

        src.add_transition_to( tgt, AlwaysTrue() )

        model = Model( 'test_model' )
        model.set_state(src)

        # TEST
        sm.run(None, model)

        # VERIFY
        self.assertEqual(tgt, model.current_state)

    def test_run_passes_start_result(self):
        # # Need to be able to send start_result to the next state
        # e.g.
        #     state place book order will check inventory straight away
        #         -   no inventory
        #         -   has inventory

        # SETUP
        sm = StateMachine( 'state machine 1' )

        tgt = State( 'tgt' )
        tgt.start  = lambda *args: 'start_result'
        tgt.run       = MagicMock()

        src = State( 'src' )
        src.add_transition_to( tgt, AlwaysTrue() )

        model = Model( 'test_model' )
        model.set_state(src)

        sm.run(None, model)

        self.assertEqual(1, tgt.run.call_count)
        self.assertEqual(None, tgt.run.call_args[0][0])
        self.assertEqual(model, tgt.run.call_args[0][1])
        self.assertEqual('start_result', model.state_start_result)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
