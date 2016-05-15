from unittest import TestCase

from state_machine.events import Event, Observer, Observable, DelayedObservable
from mock import MagicMock

class ObserverableTests(TestCase):
    ''' An implemenation of the Observer Pattern
    https://en.wikipedia.org/wiki/Observer_pattern
    '''

    def test_register_observer(self):

        observer = Observer()

        observable = Observable()
        observable.register_observer('baked',observer)

        self.assertIn( 'baked', observable.observers)
        self.assertIn( observer, observable.observers['baked'])

    def test_notify_observers(self):

        observer = Observer()
        observer.notify = MagicMock()

        observable = Observable()
        observable.register_observer('baked',observer)

        e = Event('cooked')
        observable.notify_observers(e)
        self.assertEqual(0, observer.notify.call_count)

        e = Event('baked')
        observable.notify_observers(e)
        self.assertEqual(1, observer.notify.call_count)


class DelayedObservableTests(TestCase):

    def test_notify_observers(self):
        observer = Observer()
        observer.notify = MagicMock()

        observable = DelayedObservable()
        observable.register_observer('baked',observer)

        e = Event('cooked')
        observable.notify_observers(e)
        self.assertEqual(0, observer.notify.call_count)

        e = Event('baked')
        observable.notify_observers(e)
        self.assertEqual(0, observer.notify.call_count)

        observable.flush()
        self.assertEqual(1, observer.notify.call_count)
