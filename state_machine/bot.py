from state_machine.stoppable_thread import UniqueStoppableThread, UniqueStoppableProcess
from state_machine import FinalState
from multiprocessing import Queue
import queue


class DuplicateBotException(Exception):
    pass


class Bot(object):
    """ An encapsulation of event stream and state machine instances. Each bot should
    be able to independently perform actions.
    """
    def __init__(self, event_stream_classes, machine, config):
        self.machine = machine
        self.config = config
        self.event_stream_classes = event_stream_classes
        self.event_queue = Queue()
        self.event_streams = []

    def start(self):
        self.event_streams = [fc(self.config, self.event_queue) for fc in self.event_stream_classes]
        for stream in self.event_streams:
            # Setting to daemon or the test never finishes, which is a bit of a hack,
            # but the factories should only be light processes anyway, should not be writing to
            # disks, and therefore should not cause issues if they are terminated prematurely
            stream.daemon = True
            stream.start()

    def stop(self):
        self.stop_streams()

    def stop_streams(self):
        for stream in self.event_streams:
            stream.stop()
            stream.join()

    def loop(self):
        try:
            msg = self.event_queue.get(timeout=1.0)
        except queue.Empty:
            return

        self.machine.notify(msg)
        if isinstance(self.machine.current_state, FinalState):
            self.stop()


class BotThread(Bot, UniqueStoppableThread):
    def __init__(self, event_stream_classes, machine, config):
        UniqueStoppableThread.__init__(self, machine.id)
        Bot.__init__(self, event_stream_classes, machine, config)

    def start(self):
        UniqueStoppableThread.start(self)
        Bot.start(self)

    def stop(self):
        Bot.stop(self)
        UniqueStoppableThread.stop(self)


class BotProcess(Bot, UniqueStoppableProcess):
    def __init__(self, event_stream_classes, machine, config):
        UniqueStoppableProcess.__init__(self, machine.id)
        Bot.__init__(self, event_stream_classes, machine, config)

    def start(self):
        UniqueStoppableProcess.start(self)
        Bot.start(self)

    def stop(self):
        Bot.stop(self)
        UniqueStoppableProcess.stop(self)