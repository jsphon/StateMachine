from unittest import TestCase
from state_machine.events.aggregator import EventAggregator, EventAggregatorProcess, DuplicateAggregatorException
from state_machine.events.stream import TickStream
from state_machine import StateMachine, FinalState, Event
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

        self.name = 'logmachine'
        self.logger = logging.getLogger('default')
        self.logger.setLevel(logging.DEBUG)

        formatter      = logging.Formatter('%(process)d %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)
        #self.logger.handlers[0].setFormatter(formatter)

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
        ea = EventAggregator([TickStream], machine, config)
        self.assertIsInstance(ea, EventAggregator)

    def test_start_stop(self):
        machine = MagicMock()
        config = {}

        ea = EventAggregator([TickStream], machine, config)
        ea.start()
        time.sleep(3)
        ea.stop()
        ea.join()

        self.assertFalse(ea.isAlive())

        self.assertTrue( machine.notify.call_count>0 )

    def test_start_stop2(self):
        machine = LogMachine()
        config = {}

        ea = EventAggregator([TickStream], machine, config)
        ea.start()
        time.sleep(3)
        ea.stop()

        self.assertFalse(ea.isAlive())

    def test_aggregator_stops_when_finalised(self):
        machine = LogMachine()
        config = {}

        ea = EventAggregator([TickStream], machine, config)
        ea.start()

        time.sleep(4)

        self.assertFalse(ea.is_running)
        for factory in ea.factories:
            self.assertFalse(factory.is_running)


class TestEventAggregatorProcess(TestCase):

    def test__init__(self):
        machine = MagicMock()
        config = {}
        ea = EventAggregatorProcess([TickStream], machine, config)
        self.assertIsInstance(ea, EventAggregatorProcess)

    def test_start_stop(self):
        machine = LogMachine()
        config = {}

        ea = EventAggregatorProcess([TickStream], machine, config)
        ea.start()
        time.sleep(3)
        ea.stop()

        while ea.event_queue.qsize():
            time.sleep(0.01)
        self.assertFalse(ea.is_alive())

    def test_start_autostop(self):
        machine = LogMachine()
        config = {}

        ea = EventAggregatorProcess([TickStream], machine, config)
        ea.start()

        while ea.is_alive():
            time.sleep(0.01)


        machine.logger.info('test finished')
        self.assertFalse(ea.is_alive())

    def test_prevents_multiple_starts(self):
        machine = LogMachine()
        config = {}

        machine.logger.info('Starting machine the first time, this should work')
        ea1 = EventAggregatorProcess([], machine, config)
        ea1.start()

        machine.logger.info('Starting machine the second time, this should fail')
        ea2 = EventAggregatorProcess([], machine, config)
        ea2.start()

        ea1.stop()
        ea2.stop()
        machine.logger.info('Joining ea1')
        ea1.join()
        machine.logger.info('Joining ea2')
        ea2.join()

        #self.assertTrue(ea1.is_alive())
        #self.assertFalse(ea2.is_alive())