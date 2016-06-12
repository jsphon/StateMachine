from state_machine.stoppable_thread import UniqueStoppableThread, UniqueStoppableProcess
from state_machine import FinalState
from multiprocessing import Process, Queue
import queue
import fcntl


class DuplicateBotException(Exception):
    pass


class BotThread(UniqueStoppableThread):
    ''' Listen for messages
    '''

    def __init__(self, event_stream_classes, machine, config):
        super(BotThread, self).__init__(machine.id)
        self.machine = machine
        self.event_queue = queue.Queue()
        self.event_streams = [fc(config, self.event_queue) for fc in event_stream_classes]

    def start(self):
        super(BotThread, self).start()
        for stream in self.event_streams:
            stream.start()

    def stop(self):
        super(BotThread, self).stop()
        for factory in self.event_streams:
            factory.stop()
            factory.join()

    def loop(self):
        try:
            msg = self.event_queue.get(timeout=1.0)
        except queue.Empty:
            return

        self.machine.notify(msg)
        if isinstance(self.machine.current_state, FinalState):
            self.stop()


class BotProcess(UniqueStoppableProcess):
    def __init__(self, event_stream_classes, machine, config):
        super(BotProcess, self).__init__(machine.id)
        self.machine = machine
        self.config = config
        self.event_stream_classes = event_stream_classes
        self.event_queue = Queue()
        self.event_streams = []
        self.locked_file_handle = None

    def start(self):
        super(BotProcess, self).start()

        self.event_streams = [fc(self.config, self.event_queue) for fc in self.event_stream_classes]
        for stream in self.event_streams:
            # Setting to daemon or the test never finishes, which is a bit of a hack,
            # but the factories should only be light processes anyway, should not be writing to
            # disks, and therefore should not cause issues if they are terminated prematurely
            stream.daemon = True
            stream.start()

    def stop(self):
        super(BotProcess, self).stop()
        self.stop_factories()

    def stop_factories(self):
        for factory in self.event_streams:
            factory.stop()
            factory.join()

    def loop(self):
        try:
            msg = self.event_queue.get(timeout=1.0)
        except queue.Empty:
            return

        self.machine.notify(msg)
        if isinstance(self.machine.current_state, FinalState):
            self.stop()
