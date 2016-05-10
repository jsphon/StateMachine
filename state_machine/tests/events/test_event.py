import unittest

import state_machine.events.event as event


class EventTests(unittest.TestCase):

    def test___init__(self):
        payload = {'hello':'world'}
        evt = event.Event(name='name', payload=payload)

        self.assertEqual( 'name', evt.name )
        self.assertEqual( payload, evt.payload )