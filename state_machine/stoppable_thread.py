import threading


class StoppableThread(threading.Thread):
    def __init__(self, logger=None):
        super(StoppableThread, self).__init__()

    def stop(self):
        self.is_running = False

    def loop(self):
        raise NotImplementedError()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.loop()