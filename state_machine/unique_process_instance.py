"""
Unique instance of a process, defined by id

"""

import errno
import getpass
import os

FOLDER = '/home/%s/state_machine/'%getpass.getuser()


class ProcessExistsException(Exception):
    pass


class UniqueProcessInstance(object):

    def __init__(self, id):
        self.id = id
        self.pid_folder = os.path.join(FOLDER, id)

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
