from unittest import TestCase
from state_machine.stoppable_thread import UniqueStoppableThread
from state_machine.unique_process_instance import UniqueProcessInstance, ProcessExistsException, DateTime, TIMEOUT_SECONDS
from state_machine import unique_process_instance
from unittest.mock import patch
import uuid
import os
import time
from datetime import datetime, timedelta

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
        self.assertIsInstance(self.instance, UniqueProcessInstance)

    def test_start_success(self):

        self.instance.start()

        self.assertPathExists(self.instance.pid_folder)
        self.assertPathExists(self.instance.timeout_file)

    def test_start_twice_fail(self):

        self.instance.start()

        with self.assertRaises(ProcessExistsException):
            self.instance.start()

    @patch('state_machine.unique_process_instance.DateTime')
    def test_start_twice_success(self, mock_date_time):

        utcnow = datetime.utcnow()
        mock_date_time.utcnow.return_value = utcnow
        self.instance.start()

        utcnow += timedelta(seconds=unique_process_instance.TIMEOUT_SECONDS+1)
        mock_date_time.utcnow.return_value = utcnow

        self.instance.start()

    @patch('state_machine.unique_process_instance.DateTime')
    def test_get_timeout(self, mock_date_time):
        utcnow = datetime.utcnow()
        mock_date_time.utcnow.return_value = utcnow
        self.instance.start(timeout_seconds=5)

        expected_timeout = utcnow + timedelta(seconds=5)

        actual_timeout = self.instance.get_timeout()

        self.assertEqual(expected_timeout, actual_timeout)

    def test_stop(self):
        #SETUP
        os.makedirs(self.instance.pid_folder)
        with open(self.instance.timeout_file, 'w') as f:
            f.write('')
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

    @patch('state_machine.unique_process_instance.DateTime')
    def test_create_timeout(self, mock_date_time):

        #SETUP
        os.makedirs(self.instance.pid_folder)
        utcnow = datetime.utcnow()
        mock_date_time.utcnow.return_value = utcnow
        expected_timeout = utcnow+timedelta(seconds=TIMEOUT_SECONDS)

        #TEST
        self.instance.create_timeout()

        # VERIFY
        self.assertPathExists(self.instance.timeout_file)
        with open(self.instance.timeout_file, 'r') as f:
            timeout_str = f.read()

        timeout = datetime.strptime(timeout_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertEqual(expected_timeout, timeout)

    def assertPathExists(self, path):
        self.assertTrue(os.path.exists(path))

    def assertPathDoesNotExist(self, path):
        self.assertFalse(os.path.exists(path))