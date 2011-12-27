Overview
=======
This library is provided to allow standard python logging to output log data as json objects. With JSON we can make our logs more readable by machines and we can stop writing custom parsers for syslog type records.

Installing
==========

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
