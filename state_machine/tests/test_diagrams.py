'''
Created on 24 May 2015

@author: jon
'''
import unittest
from state_machine import State, StateMachine, FinalState, CompositeState
from unittest.mock import MagicMock
import state_machine.diagrams as diagrams

class DiagramTests(unittest.TestCase):

    def setUp(self):

        chatbot = StateMachine('chatbot')
        active_state = chatbot.create_state('active', CompositeState)
        sleeping_state = chatbot.create_state('sleeping', State)
        final_state = chatbot.create_state('final', FinalState)

        chatbot.initial_state=active_state
        active_state.add_transition_to(sleeping_state, 'sunset')
        active_state.add_transition_to(final_state, 'bandwidth exceeded')

        sleeping_state.add_transition_to(active_state, 'sunrise')
        sleeping_state.add_transition_to(final_state, 'power off')

        def become_happy( event, state ):
            state.logger.info('Becoming Happy')

        def happy_message(event, state):
            if event.name=='msg':
                state.logger.info('Hello %s, I am happy', event.payload['from'])

        def become_sad(event, state):
            state.logger.info('Becoming Sad')

        def sad_message(event, state):
            if event.name=='msg':
                state.logger.info('Hello %s, I am sad', event.payload['from'])

        def sun_is_shining(event, state):
            return True

        def clouds_are_looming(event, state):
            return True

        def do_happy_dance(event, state):
            return True

        def hang_head_in_shame(event, state):
            return True

        happy_state = active_state.create_state('happy')
        happy_state.on_start = become_happy
        happy_state.on_run   = happy_message

        sad_state = active_state.create_state('sad')
        sad_state.on_start = become_sad
        sad_state.on_run = sad_message

        final_state = active_state.create_state( 'depressed', FinalState )

        happy_state.add_transition_to(sad_state, 'criticism', guard=clouds_are_looming, action=hang_head_in_shame)
        sad_state.add_transition_to(happy_state, 'praise', guard=sun_is_shining, action=do_happy_dance)
        sad_state.add_transition_to(final_state, 'excessive criticism')

        active_state.initial_state=happy_state
        active_state.initialise()

        self.chatbot = chatbot

    def test_draw_machine(self):

        G = diagrams.draw_machine(self.chatbot)

    def test_display_machine(self):
        diagrams.display_machine(self.chatbot)