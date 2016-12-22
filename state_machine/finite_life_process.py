"""

Class providing a context block to limit age,
with age limited to modulus of minutes

"""

from datetime import datetime, timedelta

class FiniteLife(object):
    """
    An object that will return is_alive=True until the next "round_minutes",
    plus delay_seconds.

    The use case for this is when, for example, a cron job is started every 5
    minutes and we want to run it continuously. It might take a second or two for
    it to start (hence the delay), but we want to prior job to stop just after the
    minute begins. And not drag on if it was itself delayed.

    """

    def __init__(self, round_minutes=1, delay_seconds=5):
        self.round_minutes = round_minutes
        self.delay_seconds = delay_seconds

    def __enter__(self):
        utcnow = datetime.utcnow()
        minutes_left = (self.round_minutes - utcnow.minute%self.round_minutes)
        t = utcnow+timedelta(minutes=minutes_left)
        self.end_time = datetime(t.year, t.month, t.day, t.hour, t.minute, self.delay_seconds)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def has_expired(self):
        return datetime.utcnow()>self.end_time

    @property
    def is_alive(self):
        return datetime.utcnow()<self.end_time



if __name__=='__main__':

    import time
    with FiniteLife(round_minutes=5) as fl:
        while fl.is_alive:
            print('%s Sleeping till %s' % (datetime.utcnow(), fl.end_time))
            time.sleep(1)
