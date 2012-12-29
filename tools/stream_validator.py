"""Stocker Stream Validator"""

import datetime
import sys

from stocker.common.events import Event
from stocker.common.utils import Stream

class TimeValidator(object):
    """Checking sequence events"""

    def __init__(self):
        self.last_event = Event()
        self.last_event.timestamp = datetime.datetime.min

    def process(self, event):
        assert event.timestamp >= self.last_event.timestamp, "Current event is earlier than previous: %r < %r" % (
        event, self.last_event)

        self.last_event = event


def main(stream_path):
    print "hello"

    tv = TimeValidator()

    for event in Stream.next_event(stream_path):
        tv.process(event)

    print "All done, seems correct"

if __name__ == "__main__":
    print "Usage:"
    print "%s <stream path>" % sys.argv[0]

    #stream_path = "C:\\code\\stocker_data\\streams\\amica_cityinter_kghm_large.stm"
    stream_path = sys.argv[1]

    main(stream_path)