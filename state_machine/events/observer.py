'''
A module implementing the observer pattern
https://en.wikipedia.org/wiki/Observer_pattern

The basic pattern is enhanced to handle named events
'''

from collections import defaultdict


class Observable(object):

    def __init__(self):
        self.__observers = defaultdict(set)

    @property
    def observers(self):
        return self.__observers

    def register_observer(self, event_name, observer):
        self.__observers[event_name].add(observer)

    def notify_observers(self, event):
        observers = self.__observers[event.name]
        for observer in observers:
            observer.notify(event)


class Observer(object):

    def notify(self, event):
        pass
