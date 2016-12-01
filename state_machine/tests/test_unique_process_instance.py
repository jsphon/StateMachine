from unittest import TestCase
from state_machine.stoppable_thread import UniqueStoppableThread
from state_machine.unique_process_instance import UniqueProcessInstance, ProcessExistsException
import uuid
import os
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

    def setUp(self):
        uid = str(uuid.uuid4())
        self.instance = UniqueProcessInstance(uid)

    def test___init__(self):
        uid = str(uuid.uuid4())
        instance = UniqueProcessInstance(uid)
        self.assertIsInstance(instance, UniqueProcessInstance)

    def test_start_success(self):
        uid = str(uuid.uuid4())
        instance = UniqueProcessInstance(uid)
        instance.start()

        r = os.path.exists(instance.pid_folder)
        self.assertTrue(r)

    def test_start_fail(self):
        uid = str(uuid.uuid4())
        instance = UniqueProcessInstance(uid)
        instance.start()

        with self.assertRaises(ProcessExistsException):
            instance.start()

    def test_stop(self):
        #SETUP
        os.makedirs(self.instance.pid_folder)

        r = os.path.exists(self.instance.pid_folder)
        self.assertTrue(r)

        #TEST
        self.instance.stop()

        #VERIFY
        r = os.path.exists(self.instance.pid_folder)
        self.assertFalse(r)

    def test_with(self):

        self.assertFalse(os.path.exists(self.instance.pid_folder))

        with self.instance:
            self.assertTrue(os.path.exists(self.instance.pid_folder))

        self.assertFalse(os.path.exists(self.instance.pid_folder))