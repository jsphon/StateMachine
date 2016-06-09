import threading
import os

class StoppableThread(threading.Thread):

    def __init__(self):
        super(StoppableThread, self).__init__()

    def stop(self):
        self.is_running = False

    def loop(self):
        raise NotImplementedError()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.loop()


class UniqueStoppableThread(threading.Thread):

    def __init__(self):
        super(UniqueStoppableThread, self).__init__()
        self.pid_file = None
        self.pid_fh = None
        self.is_running=False

    def start(self):
        self.pid_file = os.path.join('/tmp/', '%s.pid'%self.name)
        if os.path.exists(self.pid_file):
            raise KeyError('pid file %s already exists'%self.pid_file)
        else:
            with open(self.pid_file, 'w'):
                pass
        self.is_running=True
        super(UniqueStoppableThread, self).start()

    def stop(self):
        self.is_running = False
        self._remove_pid_file()

    def loop(self):
        raise NotImplementedError()

    def run(self):
        while self.is_running:
            self.loop()
        self._remove_pid_file()

    def _remove_pid_file(self):
        if os.path.exists(self.pid_file):
            try:
                os.remove(self.pid_file)
            except FileNotFoundError:
                pass
