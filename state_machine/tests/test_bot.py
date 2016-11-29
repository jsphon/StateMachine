import logging
import time
import uuid
from unittest import TestCase

from unittest.mock import MagicMock

from state_machine import StateMachine, FinalState
from state_machine.bot import BotThread, BotProcess
from state_machine.events.stream import TickStream


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


class TestBotThread(TestCase):

    def test__init__(self):
        machine = MagicMock()
        config = {}
        ea = BotThread([TickStream], machine, config)
        self.assertIsInstance(ea, BotThread)

    def test_start_stop(self):
        machine = MagicMock()
        config = {'tick_interval':0.01}

        ea = BotThread([TickStream], machine, config)
        ea.start()
        ea.stop()
        ea.join()

        self.assertFalse(ea.isAlive())
        self.assertTrue( machine.notify.call_count>0 )

    def test_start_raises_KeyError(self):
        machine = LogMachine()
        machine.name = uuid.uuid4()
        config = {'tick_interval':0.1}
        ea1 = BotThread([TickStream], machine, config)
        ea1.start()

        #TEST
        ea2 = BotThread([TickStream], machine, config)
        with self.assertRaises(KeyError):
            ea2.start()

        #TEARDOWN
        ea1.stop()

    def test_bot_stops_when_finalised(self):
        machine = LogMachine()
        machine.name = uuid.uuid4()
        config = {'tick_interval':0.01}

        ea = BotThread([TickStream], machine, config)
        ea.start()
        ea.join()

        self.assertFalse(ea.is_running)
        for stream in ea.event_streams:
            self.assertFalse(stream.is_running)


class TestBotProcess(TestCase):

    def test__init__(self):
        machine = MagicMock()
        config = {}
        ea = BotProcess([TickStream], machine, config)
        self.assertIsInstance(ea, BotProcess)

    def test_start_stop(self):
        machine = LogMachine()
        machine.name = uuid.uuid4()
        config = {'tick_interval':0.01}

        ea = BotProcess([TickStream], machine, config)
        ea.start()
        ea.stop()
        ea.join()

        self.assertFalse(ea.is_alive())

    def test_start_stops_when_finalised(self):
        machine = LogMachine()
        machine.name = uuid.uuid4()
        config = {'tick_interval':0.01}

        ea = BotProcess([TickStream], machine, config)
        ea.start()
        ea.join()

        machine.logger.info('test finished')
        self.assertFalse(ea.is_alive())

    def test_prevents_multiple_starts(self):
        machine = LogMachine()
        machine.name = uuid.uuid4()
        config = {}
        ea1 = BotProcess([TickStream], machine, config)
        ea1.start()
        time.sleep(0.1)

        # TEST
        ea2 = BotProcess([TickStream], machine, config)
        with self.assertRaises(KeyError):
            ea2.start()

        # TEARDOWN
        ea1.stop()