import re

from datetime import datetime, timedelta

import sys
sys.path.insert(0, "bindings/python/") # XXX
import elliptics

__doc__ = \
    """
    Converters from and to elliptics dnet_time format.
    """

class Time(object):
    __doc__ = \
        """
        Wrapper on top of dnet_time
        """
    __slots__ = ('time')

    def __init__(self, tsec, tnsec):
        self.time = elliptics.Time(tsec, tnsec)

    def __str__(self):
        return datetime.fromtimestamp(self.time.tsec).strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return "Time({0}, {1})".format(self.time.tsec, self.time.tnsec)

    @classmethod
    def time_min(cls):
        return cls(0, 0)

    @classmethod
    def time_max(cls):
        return cls(2**64-1, 2**64-1)

    def to_etime(self):
        return self.time

    @classmethod
    def from_epoch(cls, epoch):
        return cls(int(epoch), 0)

    @classmethod
    def from_etime(cls, etime):
        return cls(etime.tsec, etime.tnsec)

    @classmethod
    def from_datetime(cls, dt):
        epoch = (dt - datetime(1970, 1, 1)).total_seconds()
        return cls.from_epoch(epoch)

    @classmethod
    def from_string(cls, string):
        """
        Parses human readable input into time difference from datetime.now()

        >>> Time.from_string("3w")
        Time(1367989070, 0)
        >>> Time.from_string("3w 12h 57m")
        Time(1367942475, 0)
        """
        keys = ["weeks", "days", "hours", "minutes"]
        regex = "".join(["((?P<%s>\d+)%s ?)?" % (k, k[0]) for k in keys])
        kwargs = {}
        for k,v in re.match(regex, string).groupdict(default=0).items():
            kwargs[k] = int(v)
        dt = datetime.utcnow() - timedelta(**kwargs)
        return cls.from_datetime(dt)
