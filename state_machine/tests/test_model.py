import unittest
from state_machine.model import Model
from state_machine.constants import CURRENT_STATE_NAME, CURRENT_STATE_COMMENT, CURRENT_STATE_INPUT, CURRENT_STATE_START_RESULT
from mock import MagicMock

class ModelTests(unittest.TestCase):

    def test___init__(self):
        m = Model( 'test_model' )

    def test_recover_state(self):

        state1 = MagicMock()
        state2 = MagicMock()

        machine = MagicMock()
        machine.states = { 's1':state1, 's2':state2 }

        m = Model( 'test_model' )

        # First Test
        m.load_state_name = MagicMock( return_value='s1' )
        m.recover_state( machine )
        self.assertEqual( state1, m.current_state )

        # Second Test
        m.load_state_name = MagicMock( return_value='s2' )
        m.recover_state( machine )
        self.assertEqual( state2, m.current_state )

    def test_set_state(self):
        model   = Model( 'test model' )

        state1  = MagicMock()
        state1.name = 'test state'
        #state_input = 'state_input'
        start_result = 'start_result'

        model.set_state(state1, start_result)

        self.assertEqual( state1, model.current_state )
        #self.assertEqual( state_input, model.state_input )
        self.assertEqual( start_result, model.state_start_result )

        print( 'finished test_set_state' )

    def test_set_state_comment(self):
        model   = Model( 'test model'  )
        model.set_state_comment( 'foobar' )