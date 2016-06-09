from state_machine.stoppable_thread import UniqueStoppableThread
from state_machine import  FinalState
from multiprocessing import Process, Queue
import queue
import fcntl

class DuplicateAggregatorException(Exception):
    pass

class EventAggregator(UniqueStoppableThread):
    ''' Listen for messages
    '''

    def __init__(self, event_factory_classes, machine, config):
        super(EventAggregator, self).__init__()
        self.machine = machine
        self.event_queue = queue.Queue()
        self.factories = [fc(config, self.event_queue) for fc in event_factory_classes]
        self.name = machine.id

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


class EventAggregatorProcess(Process):

    def __init__(self, event_factory_classes, machine, config):
        super(EventAggregatorProcess, self).__init__()
        self.machine = machine
        self.config = config
        self.event_factory_classes = event_factory_classes
        self.event_queue = Queue()
        self.factories = []
        self.locked_file_handle = None


    def start(self):
        super(EventAggregatorProcess, self).start()

        self.factories = [fc(self.config, self.event_queue) for fc in self.event_factory_classes]
        for factory in self.factories:
            # Setting to daemon or the test never finishes, which is a bit of a hack,
            # but the factories should only be light processes anyway, should not be writing to
            # disks, and therefore should not cause issues if they are terminated prematurely
            factory.daemon=True
            factory.start()

    def stop(self):
        self.stop_factories()
        self.event_queue.put(None)

    def stop_factories(self):
        for factory in self.factories:
            factory.stop()
            factory.join()

    def run(self):
        is_stopped=False

        try:
            self.locked_file_handle = lock_file(self.machine.id)
        except IOError:
            self.machine.logger.error('Cannot start %s as it is already locked'%self.machine.id)
            self.stop_factories()
            return

        self.machine.logger.info('Running %s'%self.machine.id)

        while not is_stopped:
            msg = self.event_queue.get()
            if msg:
                self.machine.notify(msg)
                if isinstance(self.machine.current_state, FinalState):
                    self.stop()
            else:
                self.machine.logger.info('EventAggregatorProcess received poison pill.')
                is_stopped=True


def lock_file(process_id):
    pid_file = '/tmp/program_%s.pid'%process_id
    print('Locking %s'%pid_file)
    fp = open(pid_file, 'w')
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    return fp