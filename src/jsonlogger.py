import logging, json, re

class JsonFormatter(logging.Formatter):
    def format(self, record):
        logRecord = record.__dict__

        formatterParse = re.compile(r'\((.*?)\)', re.IGNORECASE)
        formatters = formatterParse.findall(self._fmt)
        
        if formatters[0] == 'message':
            logRecord = {'message': record.msg}
        
        return json.dumps(logRecord)

