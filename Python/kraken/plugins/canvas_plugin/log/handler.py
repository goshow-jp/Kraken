import logging


class DCCHandler(logging.StreamHandler):
    """Logging Handler for Canvas."""

    def __init__(self, stream=None):
        super(DCCHandler, self).__init__(stream)

    def emit(self, record):
        msg = self.format(record)
        print msg
