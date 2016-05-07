
import unittest

from state_machine.state_machine import StateMachine
from state_machine.exception import StateMachineException
from state_machine.state import State
from state_machine.condition import ALWAYS_TRUE, ALWAYS_FALSE, AlwaysTrue
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

        src.add_transition_to( tgt, ALWAYS_TRUE )

        model = Model( 'test_model' )
        model.set_state(src)

        data = {ALWAYS_TRUE.listens_for:1}

        # TEST
        sm.run(data, model)

        # VERIFY
        self.assertEqual(tgt, model.current_state)

    def test_run_passes_start_result(self):
        # # Need to be able to send start_result to the next state
        # e.g.
        #     state place book order will check inventory straight away
        #         -   no inventory
        #         -   has inventory

        sm = StateMachine( 'state machine 1' )

        state_wait = State( 'Wait State' )

        state_action = State('Action State')
        state_action.on_start = lambda *arg, **kwargs: 'action result'

        state_final = State('Final State')
        state_final.on_start = lambda data, model, state_input:{'final state input':state_input}

        state_wait.add_default_transition_to(state_action)
        state_action.add_default_transition_to(state_final)

        model = Model( 'test_model' )
        model.set_state(state_wait)

        data = {ALWAYS_TRUE.listens_for:1}
        sm.run(data, model)

        model.logger.info( 'We are in state %s',model.current_state)
        model.logger.info( 'State input ''%s''',model.current_state_input)
        self.assertEqual( 'action result', model.current_state_input)
        self.assertEqual( {'final state input':'action result'}, model.current_state_start_result)

    def test_run_splits_streams_correctly(self):

        sm = StateMachine('test machine')

        src = State( 'src' )
        tgt1 = State( 'tgt1' )
        tgt2 = State('tgt2')

        c1  = AlwaysTrue()
        c1.listens_for = 'stream1'

        c2 = AlwaysTrue()
        c2.listens_for = 'stream2'

        src.add_transition_to( tgt1, c1 )
        src.add_transition_to( tgt2, c2 )

        model = Model( 'test' )

        # Test1
        model.set_state(src)
        sm.run( {'stream1':1}, model )
        self.assertEqual(tgt1, model.current_state)

        # Test2
        model.set_state(src)
        sm.run( {'stream2':1}, model )
        self.assertEqual(tgt2, model.current_state)

        # Test3
        model.set_state(src)
        sm.run( {'none':1}, model )
        self.assertEqual(src, model.current_state)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
