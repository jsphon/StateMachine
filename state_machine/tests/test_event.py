import unittest

import state_machine.event as event
import logging

class EventTests(unittest.TestCase):

    def test___init__(self):
        payload = {'hello':'world'}
        evt = event.Event(name='name', payload=payload)

        self.assertEqual( 'name', evt.name )
        self.assertEqual( payload, evt.payload )