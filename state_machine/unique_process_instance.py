"""
Unique instance of a process, defined by id

"""

from datetime import datetime, timedelta
import errno
import getpass
import os
import time
import logging

FOLDER = '/home/%s/state_machine/'%getpass.getuser()
TIMEOUT_SECONDS = 300

class ProcessExistsException(Exception):
    pass


class UniqueProcessInstance(object):

    def __init__(self, id):
        self.id = id
        self.pid_folder = os.path.join(FOLDER, id)
        self.timeout_file = os.path.join(self.pid_folder, 'timeout')

    def __enter__(self):
        self.start()

    def __exit__(self, type_, value, traceback):
        self.stop()

    def start(self, timeout_seconds=TIMEOUT_SECONDS):
        try:
            os.makedirs(self.pid_folder)
        except Exception as e:
            if DateTime.utcnow() > self.get_timeout():
                self.stop()
                self.start()
            elif e.errno == errno.EEXIST:
                raise ProcessExistsException('Process %s already exists'%self.id)
            else:
                raise
        else:
            # Only called if no exception
            self.create_timeout(timeout_seconds)

    def stop(self):
        os.remove(self.timeout_file)
        os.rmdir(self.pid_folder)

    def create_timeout(self, timeout_seconds=TIMEOUT_SECONDS):
        timeout = DateTime.utcnow() + timedelta(seconds=timeout_seconds)
        with open(self.timeout_file, 'w') as f:
            f.write(timeout.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

    def get_timeout(self):
        if os.path.exists(self.timeout_file):
            with open(self.timeout_file, 'r') as f:
                sdate = f.read()
            return datetime.strptime(sdate, '%Y-%m-%dT%H:%M:%S.%fZ')


class RetryingUniqueProcessInstance(UniqueProcessInstance):

    def __init__(self, uid, max_retries=3, delay=1.0):
        super(RetryingUniqueProcessInstance, self).__init__(uid)
        self.max_retries = max_retries
        self.delay = delay

    def start(self):
        self._try_to_start(self.max_retries)

    def _try_to_start(self, attempts_remaining):

        try:
            s = super(RetryingUniqueProcessInstance, self)
            s.start()
        except ProcessExistsException as e:
            if attempts_remaining > 0:
                logging.info('%s already running, waiting %i seconds', self.id, self.delay)
                time.sleep(self.delay)
                self._try_to_start(attempts_remaining-1)
            else:
                raise e


class DateTime(datetime):
    pass
