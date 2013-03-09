import logging
import json
import re

#Support order in python 2.7 and 3
try:
    from collections import OrderedDict
except:
    pass

class JsonFormatter(logging.Formatter):
    """A custom formatter to format logging records as json objects"""

    def parse(self):
        standard_formatters = re.compile(r'\((.*?)\)', re.IGNORECASE)
        return standard_formatters.findall(self._fmt)

    def format(self, record):
        """Formats a log record and serializes to json"""

        formatters = self.parse()

        record.message = record.getMessage()
        # only format time if needed
        if "asctime" in formatters:
            record.asctime = self.formatTime(record, self.datefmt)

        try:
            log_record = OrderedDict()
        except:
            log_record = {}

        for formatter in formatters:
            log_record[formatter] = record.__dict__[formatter]

        return json.dumps(log_record)
