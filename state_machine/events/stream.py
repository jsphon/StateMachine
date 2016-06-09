import datetime, time

from state_machine.events import Event
from state_machine.stoppable_thread import StoppableThread

class EventStream(StoppableThread):

    def __init__(self, config, event_queue):
        super(StoppableThread, self).__init__()
        self.event_queue=event_queue


class TickStream(EventStream):

    def __init__(self, config, event_queue):
        super(TickStream, self).__init__(config, event_queue)
        self.interval = config.get('tick_interval', 1.0)

    def loop(self):
        e = Event('tick', datetime.datetime.utcnow())
        self.event_queue.put(e)
        time.sleep(self.interval)