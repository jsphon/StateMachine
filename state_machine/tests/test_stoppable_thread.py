from unittest import TestCase
from state_machine.stoppable_thread import UniqueStoppableThread
import uuid
import time

import logging
logger = logging.getLogger('default')
logger.addHandler(logging.StreamHandler())

class MockThread(UniqueStoppableThread):

    def __init__(self, name):
        super(MockThread, self).__init__()
        self.name=name

    def loop(self):
        logger.info('loop')
        time.sleep(1)

class TestUniqueStoppableThread(TestCase):

    def test_start_stop(self):
        thread_name = uuid.uuid4()
        t = MockThread(thread_name)
        logger.info('Starting')
        t.start()

        self.assertTrue(t.is_running)
        self.assertTrue(t.is_alive())

        time.sleep(0.1)

        logger.info('Stopping')
        t.stop()
        t.join()
        self.assertFalse(t.is_running)
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