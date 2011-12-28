import logging
import json
import re
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """A custom formatter to format logging records as json objects"""

    def format(self, record):
        """Formats a log record and serializes to json"""
        mappings = {
            'asctime': create_timestamp,
            'message': lambda r: r.msg,
        }

        standard_formatters = re.compile(r'\((.*?)\)', re.IGNORECASE)
        formatters = standard_formatters.findall(self._fmt)
        
        log_record = {}
        for formatter in formatters:
            try:
                log_record[formatter] = mappings[formatter](record)
            except KeyError:
                log_record[formatter] = record.__dict__[formatter]

        return json.dumps(log_record)

def create_timestamp(record):
    """Creates a human readable timestamp for a log records created date"""
    
    timestamp = datetime.fromtimestamp(record.created)
    return timestamp.strftime("%y-%m-%d %H:%M:%S,%f"),
