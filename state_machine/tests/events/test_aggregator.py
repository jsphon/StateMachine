from unittest import TestCase
from state_machine.events.aggregator import EventAggregator, EventFactory, TickFactory
from state_machine import StateMachine, FinalState
from mock import MagicMock
import time
import logging

def under_3_logs(event, state):
    return state.vars['log_count']<3

def three_or_more_logs(event, state):
    return state.vars['log_count']>=3

def log_event(event, state):
    state.logger.info(event)
    state.vars['log_count']+=1

class LogMachine(StateMachine):

    def __init__(self):
        super(LogMachine, self).__init__()

        self.logger = logging.getLogger('default')
        self.logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        self.logger.addHandler(sh)

        s1 = self.create_state('log event')
        s2 = self.create_state('final', FinalState)

        self.initial_state = s1
        self.initialise()

        s1.add_transition_to(s1, 'tick', guard=under_3_logs, action=log_event)
        s1.add_transition_to(s2, 'tick', guard=three_or_more_logs)

        self.vars['log_count']=0

class TestEventAggregator(TestCase):

    def test__init__(self):
        machine = MagicMock()
        config = {}
        ea = EventAggregator([TickFactory], machine, config)
        self.assertIsInstance(ea, EventAggregator)

    def test_start_stop(self):
        machine = MagicMock()
        config = {}

        ea = EventAggregator([TickFactory], machine, config)
        ea.start()
        time.sleep(3)
        ea.stop()

        self.assertFalse(ea.isAlive())

        self.assertTrue( machine.notify.call_count>0 )

    def test_start_stop2(self):
        machine = LogMachine()
        config = {}

        ea = EventAggregator([TickFactory], machine, config)
        ea.start()
        time.sleep(3)
        ea.stop()

        self.assertFalse(ea.isAlive())

    def test_aggregator_stops_when_finalised(self):
        machine = LogMachine()
        config = {}

        ea = EventAggregator([TickFactory], machine, config)
        ea.start()

        time.sleep(4)

        self.assertFalse(ea.is_running)
        for factory in ea.factories:
            self.assertFalse(factory.is_running)