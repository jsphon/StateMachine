from unittest import TestCase
from state_machine.events.stream import TickStream

import threading
import queue
import time
import logging
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

class TestTickStream(TestCase):

    def test_xxx(self):

        logger.info('# Threads:%i',threading.active_count())

        event_queue = queue.Queue()
        cfg = {}
        f = TickStream(cfg, event_queue)

        f.start()
        time.sleep(3)

        logger.info('# Threads:%i',threading.active_count())
        f.stop()

        time.sleep(1)

        logger.info(event_queue.qsize())
        logger.info(f.is_alive())
        logger.info('# Threads:%i',threading.active_count())