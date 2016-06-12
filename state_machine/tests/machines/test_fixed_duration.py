import datetime
from unittest import TestCase
import state_machine.machines.fixed_duration as mod
from state_machine import Event


class FixedDurationMachineTests(TestCase):

    def setUp(self):
        self.machine = mod.FixedDurationMachine()
        self.machine.initialise()

    def test___init__(self):
        self.assertIsInstance(self.machine, mod.FixedDurationMachine)

    def test_tick_before_threshold(self):
        e = Event('tick', datetime.datetime.utcnow())

        self.machine.notify(e)

        self.assertEqual('tick', self.machine.current_state.name)

    def test_tick_after_threshold(self):
        e = Event('tick', self.machine.date_threshold+datetime.timedelta(1))

        self.machine.notify(e)

        self.assertEqual('final', self.machine.current_state.name)

    def test_on_tick(self):

        has_ticked=False
        def on_tick(event, state):
            nonlocal has_ticked
            has_ticked=True
            state.logger.info('loop')

        self.machine.on_tick = on_tick
        e = Event('tick', datetime.datetime.utcnow())

        self.machine.notify(e)

        self.assertTrue(has_ticked)