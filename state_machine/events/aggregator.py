from state_machine.stoppable_thread import StoppableThread
from state_machine import  FinalState
import queue


class EventAggregator(StoppableThread):
    ''' Listen for messages
    '''

    def __init__(self, event_factory_classes, machine, config):
        super(EventAggregator, self).__init__()
        self.machine = machine
        self.event_queue = queue.Queue()
        self.factories = [fc(config, self.event_queue) for fc in event_factory_classes]


    def start(self):
        super(EventAggregator, self).start()
        for factory in self.factories:
            factory.start()

    def stop(self):
        super(EventAggregator, self).stop()
        for factory in self.factories:
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