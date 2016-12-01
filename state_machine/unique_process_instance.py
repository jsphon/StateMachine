"""
Unique instance of a process, defined by id

"""

from datetime import datetime, timedelta
import errno
import getpass
import os

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

    def start(self):
        try:
            os.makedirs(self.pid_folder)
        except Exception as e:
            if e.errno==errno.EEXIST:
                raise ProcessExistsException('Process %s already exists'%self.id)
            raise

    def stop(self):
        self._remove_pid_folder()

    def _remove_pid_folder(self):
        os.rmdir(self.pid_folder)

    def create_timeout(self, timeout_seconds=TIMEOUT_SECONDS):
        timeout = DateTime.utcnow() + timedelta(seconds=timeout_seconds)
        with open(self.timeout_file, 'w') as f:
            f.write(timeout.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

class DateTime(datetime):
    pass