import logging, json, re
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def create_timestamp(record):
        timestamp = datetime.fromtimestamp(record.created)
        return timestamp.strftime("%y-%m-%d %H:%M:%S,%f"),

    mappings = {
        'asctime': create_timestamp,
        'message': lambda r: r.msg,
    }

    def format(self, record):
        formatterParse = re.compile(r'\((.*?)\)', re.IGNORECASE)
        formatters = formatterParse.findall(self._fmt)
        
        logRecord = {}
        for formatter in formatters:
            try:
                logRecord[formatter] = self.mappings[formatter](record);
            except KeyError:
                logRecord[formatter] = record.__dict__[formatter]

        return json.dumps(logRecord)

