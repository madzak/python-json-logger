Overview
=======
This library is provided to allow standard python logging to output log data as json objects. With JSON we can make our logs more readable by machines and we can stop writing custom parsers for syslog type records.

Installing
==========
Pip:

    pip install python-json-logger

Pypi:

   https://pypi.python.org/pypi/python-json-logger 

Manual:

    python setup.py install

Usage
=====

Json outputs are provided by the JsonFormatter logging formatter. You can add the customer formatter like below:

```python
    import logging
    import jsonlogger

    logger = logging.getLogger()

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
```
The fmt parser can also be overiden if you want to use an alternate from the default.

```python
    class CustomJsonFormatter(jsonlogger.JsonFormatter):
      def parse(self):
          return eval(self._fmt)
```

You can also add extra fields to your json output by specifying a dict in place of message, as well as by specifying an extra={} argument.
Contents of these dictionaries will be added at the root level of the entry and may override basic fields.
For custom handling of object serialization you can specify default json object translator or provide a custom encoder

```python
    def json_translate(obj):
        if isinstance(obj, MyClass):
            return {"special": obj.special}

    formatter = jsonlogger.JsonFormatter(json_default=json_translate,
                                         json_encoder=json.JSONEncoder())
    logHandler.setFormatter(formatter)

    logger.info({"special": "value", "run": 12})
    logger.info("classic message", extra={"special": "value", "run": 12})
```

Example
=======

Sample JSON with a full formatter (basically the log message from the unit test). Every log message will appear on 1 line like a typical logger.

```json
{
    "threadName": "MainThread", 
    "name": "root", 
    "thread": 140735202359648, 
    "created": 1336281068.506248, 
    "process": 41937, 
    "processName": "MainProcess", 
    "relativeCreated": 9.100914001464844, 
    "module": "tests", 
    "funcName": "testFormatKeys", 
    "levelno": 20, 
    "msecs": 506.24799728393555, 
    "pathname": "tests/tests.py", 
    "lineno": 60, 
    "asctime": ["12-05-05 22:11:08,506248"], 
    "message": "testing logging format", 
    "filename": "tests.py", 
    "levelname": "INFO",
    "special": "value",
    "run": 12
}
```
