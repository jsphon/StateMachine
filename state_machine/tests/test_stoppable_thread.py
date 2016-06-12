from unittest import TestCase
from state_machine.stoppable_thread import UniqueStoppableThread
import state_machine.stoppable_thread as mod
import uuid
import time

import logging
logger = logging.getLogger('default')
logger.addHandler(logging.StreamHandler())

class MockThread(UniqueStoppableThread):

    def __init__(self, id):
        super(MockThread, self).__init__(id)

    def loop(self):
        logger.info('loop')
        time.sleep(0.1)


class TestUniqueStoppableThread(TestCase):

    def test_start_stop(self):
        thread_name = uuid.uuid4()
        t = MockThread(thread_name)
        logger.info('Starting')
        t.start()

        self.assertTrue(t._is_running)
        self.assertTrue(t.is_alive())

        time.sleep(0.1)

        logger.info('Stopping')
        t.stop()
        t.join()
        self.assertFalse(t._is_running)
        self.assertFalse(t.is_alive())

    def test_start_raises_KeyError(self):

        # SETUP
        thread_name = uuid.uuid4()

        t1 = MockThread(thread_name)
        t1.start()

        self.assertTrue(t1.is_alive())

        # TEST/VERIFY
        t2 = MockThread(thread_name)
        with self.assertRaises(KeyError):
            t2.start()

        # TEAR DOWN
        t1.stop()


class MockStoppableProcess(mod.StoppableProcess):

    def __init__(self):
        super(MockStoppableProcess, self).__init__()

    def loop(self):
        logger.info('loop')
        time.sleep(1)


class TestStoppableProcess(TestCase):

    def test___init__(self):
        MockStoppableProcess()

    def test_start(self):
        p = MockStoppableProcess()
        p.start()

        self.assertTrue(p.is_alive())

        p.terminate()

    def test_stop(self):
        p = MockStoppableProcess()
        p.start()
        p.stop()
        p._is_running=False
        p.join()

        self.assertFalse(p.is_alive())


class MockUniqueStoppableProcess(mod.UniqueStoppableProcess):

    def __init__(self, id):
        super(MockUniqueStoppableProcess, self).__init__(id)

    def loop(self):
        logger.info('loop')
        time.sleep(1)


class TestUniqueStoppableProcess(TestCase):

    def test_start_raises_KeyError(self):

        # SETUP
        process_id = uuid.uuid4()

        t1 = MockUniqueStoppableProcess(process_id)
        t1.start()

        self.assertTrue(t1.is_alive())

        # TEST/VERIFY
        t2 = MockThread(process_id)
        with self.assertRaises(KeyError):
            t2.start()

        # TEAR DOWN
        t1.stop()