'''
A module implementing the observer pattern
https://en.wikipedia.org/wiki/Observer_pattern

The basic pattern is enhanced to handle named events
'''

from collections import defaultdict


class Observable(object):

    def __init__(self):
        self._observers = defaultdict(set)

    @property
    def observers(self):
        return self._observers

    def register_observer(self, event_name, observer):
        self._observers[event_name].add(observer)

    def notify_observers(self, event):
        observers = self._observers[event.name]
        for observer in observers:
            observer.notify(event)


class DelayedObservable(Observable):

    def __init__(self):
        super(DelayedObservable,self).__init__()
        self.queue=[]

    def notify_observers(self, event):
        self.queue.append(event)

    def flush(self):
        while self.queue:
            event = self.queue.pop(0)
            super(DelayedObservable,self).notify_observers(event)

class Observer(object):

    def notify(self, event):
        pass
