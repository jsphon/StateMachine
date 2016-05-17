
import unittest

from state_machine.state_machine import StateMachine
from state_machine.exception import StateMachineException
from state_machine.state import State, PseudoState
from state_machine import Event
from mock import MagicMock


class StateMachineTests(unittest.TestCase):

    def test___init__(self):
        sm = StateMachine( 'test machine' )
        self.assertIsInstance(sm, StateMachine)

    def test_add_state(self):

        state = MagicMock()
        state.name='test_state'

        sm = StateMachine( 'test machine' )
        sm.add_state( state )

        self.assertEqual( state, sm.states[ 'test_state' ] )

        with self.assertRaises( StateMachineException ):
            sm.add_state( state )

    def test_notify_simple(self):
        '''
        A simple example of using a state machine
        '''

        sm  = StateMachine( 'state machine 1' )
        src = sm.create_state('src')
        tgt = sm.create_state('tgt')

        src.add_transition_to( tgt )

        sm.initial_state=src
        sm.reset()

        evt  = Event()

        # TEST
        sm.notify(evt)

        # VERIFY
        self.assertEqual(tgt, sm.current_state)

    def test_notify_splits_streams_correctly(self):

        sm = StateMachine('test machine')

        src  = sm.create_state('src')
        tgt1 = sm.create_state('tgt1')
        tgt2 = sm.create_state('tgt2')

        src.add_transition_to( tgt1, 'stream1' )
        src.add_transition_to( tgt2, 'stream2' )

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

    def test_notify_with_PseudoState(self):

        sm = StateMachine('test machine')

        src  = sm.create_state('src')
        ps   = sm.create_state('ps', PseudoState)
        tgt = sm.create_state('tgt')

        src.add_transition_to( ps )
        ps.add_transition_to( tgt )

        sm.set_state(src)

        # Test1
        e = Event()
        sm.notify(e)

        self.assertEqual(tgt, sm.current_state)

    def test_notify_with_PseudoState_can_store_vars(self):
        '''
        Test that on_start can store data in vars.
        '''

        def on_start(event, state):
            state.vars['payload']=event.payload

        sm = StateMachine('test machine')

        src  = sm.create_state('src')
        ps   = sm.create_state('ps', PseudoState)

        src.add_transition_to( ps )
        ps.on_start = on_start

        sm.set_state(src)

        # Test1
        e = Event('test', 'payload')
        sm.notify(e)

        #self.assertEqual(tgt, sm.current_state)
        self.assertEqual('payload', ps.vars['payload'])

    def test_notify_with_PseudoState_can_make_choice(self):
        '''
        Test that pseudo choice can make a choice using on_start result
        '''

        def on_start(event, state):
            state.vars['payload']=event.payload

        sm = StateMachine('test machine')

        src  = sm.create_state('src')
        ps   = sm.create_state('ps', PseudoState)
        tgt1 = sm.create_state('tgt1')
        tgt2 = sm.create_state('tgt2')

        src.add_transition_to(ps)

        ps.on_start = on_start
        guard1 = lambda evt, st: st.vars['payload']=='tgt1'
        ps.add_transition_to(tgt1, guard=guard1)

        guard2 = lambda evt, st: st.vars['payload']=='tgt2'
        ps.add_transition_to(tgt2, guard=guard2)

        # Test1
        sm.set_state(src)
        e = Event('test', 'tgt1')
        sm.notify(e)
        self.assertEqual(tgt1, sm.current_state)

        # Test2
        sm.set_state(src)
        e = Event('test', 'tgt2')
        sm.notify(e)
        self.assertEqual(tgt2, sm.current_state)

    def test_create_state(self):

        sm        = StateMachine('test')
        new_state = sm.create_state('new state')

        self.assertIsInstance(new_state, State)
        self.assertEqual('new state', new_state.name)
        self.assertEqual(new_state, sm.states['new state'])

    def test_create_state_with_custom_class(self):

        class CustomStateClass(State):

            def __init__(self, name, machine, arg0, arg1):
                super(CustomStateClass, self).__init__(name, machine)
                self.arg0=arg0
                self.arg1=arg1

        sm        = StateMachine('test')
        new_state = sm.create_state('new state', CustomStateClass, 0, arg1=1)

        self.assertIsInstance(new_state, CustomStateClass)
        self.assertEqual('new state', new_state.name)
        self.assertEqual(0, new_state.arg0)
        self.assertEqual(1, new_state.arg1)
        self.assertEqual(new_state, sm.states['new state'])

class Examples(unittest.TestCase):

    def test_inter_machine_communication(self):
        '''
        Create two state machines
         - server
         - client
        client listens to server using register_observer
        when server sends a data event, client gets notified.


        '''

        def send_data(event, state):
            state.logger.info( 'Server sending data' )
            e = Event('data', 'hello world')
            state.notify_observers(e)

        server       = StateMachine()
        server_state = server.create_state('do something')
        server_state.on_run = send_data
        server.initial_state = server_state
        server.reset()

        def handle_data(event, state):
            state.logger.info( 'Received data %s', event.payload)
            state.vars['call_count']+=1

        client = StateMachine()
        server.register_observer('data', client)
        client_state = client.create_state('wait for data')
        client_state.on_run = handle_data
        client_state.vars['call_count'] = 0

        client.initial_state = client_state
        client.reset()

        # Test
        e = Event('tick')
        server.notify(e)

        # Verify
        self.assertEqual(1, client_state.vars['call_count'])

        # Test Again!
        server.notify(e)
        self.assertEqual(2, client_state.vars['call_count'])



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
