import threading
import os

import ctypes
import multiprocessing


class StoppableThread(threading.Thread):

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._is_running=False

    def start(self):
        self._is_running=True
        threading.Thread.start(self)

    def stop(self):
        self._is_running = False

    def run(self):
        while self._is_running:
            self.loop()

    def loop(self):
        raise NotImplementedError()


class StoppableProcess(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self._is_running = multiprocessing.Value(ctypes.c_bool, False )

    def start(self):
        multiprocessing.Process.start(self)
        self._is_running.value=True

    def stop(self):
        self._is_running.value=False

    def run(self):
        while self._is_running.value:
            self.loop()

    def loop(self):
        raise NotImplementedError()


class Unique(object):

    def __init__(self):
        self.pid_file = None
        self.pid_fh = None
        self.name = 'default'

    def start(self):
        self.pid_file = os.path.join('/tmp/', '%s.pid'%self.name)
        if os.path.exists(self.pid_file):
            raise KeyError('pid file %s already exists'%self.pid_file)
        else:
            open(self.pid_file, 'w')

    def on_stop(self):
        self._remove_pid_file()

    def _remove_pid_file(self):
        if os.path.exists(self.pid_file):
            try:
                os.remove(self.pid_file)
            except FileNotFoundError:
                pass

class UniqueStoppableThread(StoppableThread, Unique):

    def __init__(self):
        StoppableThread.__init__(self)
        Unique.__init__(self)

    def start(self):
        Unique.start( self )
        StoppableThread.start(self)

    def run(self):
        StoppableThread.run(self)
        Unique.on_stop(self)
