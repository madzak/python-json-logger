# -*- coding: utf-8 -*-
import unittest
import unittest.mock
import logging
import json
import sys
import traceback
import random

try:
    import xmlrunner  # noqa
except ImportError:
    pass

try:
    from StringIO import StringIO  # noqa
except ImportError:
    # Python 3 Support
    from io import StringIO

sys.path.append('src/python-json-logger')
from pythonjsonlogger import jsonlogger
import datetime


class TestJsonLogger(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("logging-test-{}".format(random.randint(1, 101)))
        self.logger.setLevel(logging.DEBUG)
        self.buffer = StringIO()

        self.logHandler = logging.StreamHandler(self.buffer)
        self.logger.addHandler(self.logHandler)

    def testDefaultFormat(self):
        fr = jsonlogger.JsonFormatter()
        self.logHandler.setFormatter(fr)

        msg = "testing logging format"
        self.logger.info(msg)
        logJson = json.loads(self.buffer.getvalue())

        self.assertEqual(logJson["message"], msg)

    def testRenameBaseField(self):
        fr = jsonlogger.JsonFormatter(rename_fields={'message': '@message'})
        self.logHandler.setFormatter(fr)

        msg = "testing logging format"
        self.logger.info(msg)
        logJson = json.loads(self.buffer.getvalue())

        self.assertEqual(logJson["@message"], msg)

    def testFormatKeys(self):
        supported_keys = [
            'asctime',
            'created',
            'filename',
            'funcName',
            'levelname',
            'levelno',
            'lineno',
            'module',
            'msecs',
            'message',
            'name',
            'pathname',
            'process',
            'processName',
            'relativeCreated',
            'thread',
            'threadName'
        ]

        log_format = lambda x: ['%({0:s})s'.format(i) for i in x]
        custom_format = ' '.join(log_format(supported_keys))

        fr = jsonlogger.JsonFormatter(custom_format)
        self.logHandler.setFormatter(fr)

        msg = "testing logging format"
        self.logger.info(msg)
        log_msg = self.buffer.getvalue()
        log_json = json.loads(log_msg)

        for supported_key in supported_keys:
            if supported_key in log_json:
                self.assertTrue(True)

    def testUnknownFormatKey(self):
        fr = jsonlogger.JsonFormatter('%(unknown_key)s %(message)s')

        self.logHandler.setFormatter(fr)
        msg = "testing unknown logging format"
        try:
            self.logger.info(msg)
        except:
            self.assertTrue(False, "Should succeed")

    def testLogADict(self):
        fr = jsonlogger.JsonFormatter()
        self.logHandler.setFormatter(fr)

        msg = {"text": "testing logging", "num": 1, 5: "9",
               "nested": {"more": "data"}}
        self.logger.info(msg)
        logJson = json.loads(self.buffer.getvalue())
        self.assertEqual(logJson.get("text"), msg["text"])
        self.assertEqual(logJson.get("num"), msg["num"])
        self.assertEqual(logJson.get("5"), msg[5])
        self.assertEqual(logJson.get("nested"), msg["nested"])
        self.assertEqual(logJson["message"], None)

    def testLogExtra(self):
        fr = jsonlogger.JsonFormatter()
        self.logHandler.setFormatter(fr)

        extra = {"text": "testing logging", "num": 1, 5: "9",
                 "nested": {"more": "data"}}
        self.logger.info("hello", extra=extra)
        logJson = json.loads(self.buffer.getvalue())
        self.assertEqual(logJson.get("text"), extra["text"])
        self.assertEqual(logJson.get("num"), extra["num"])
        self.assertEqual(logJson.get("5"), extra[5])
        self.assertEqual(logJson.get("nested"), extra["nested"])
        self.assertEqual(logJson["message"], "hello")

    def testJsonDefaultEncoder(self):
        fr = jsonlogger.JsonFormatter()
        self.logHandler.setFormatter(fr)

        msg = {"adate": datetime.datetime(1999, 12, 31, 23, 59),
               "otherdate": datetime.date(1789, 7, 14),
               "otherdatetime": datetime.datetime(1789, 7, 14, 23, 59),
               "otherdatetimeagain": datetime.datetime(1900, 1, 1)}
        self.logger.info(msg)
        logJson = json.loads(self.buffer.getvalue())
        self.assertEqual(logJson.get("adate"), "1999-12-31T23:59:00")
        self.assertEqual(logJson.get("otherdate"), "1789-07-14")
        self.assertEqual(logJson.get("otherdatetime"), "1789-07-14T23:59:00")
        self.assertEqual(logJson.get("otherdatetimeagain"),
                         "1900-01-01T00:00:00")

    @unittest.mock.patch('time.time', return_value=1500000000.0)
    def testJsonDefaultEncoderWithTimestamp(self, time_mock):
        fr = jsonlogger.JsonFormatter(timestamp=True)
        self.logHandler.setFormatter(fr)

        self.logger.info("Hello")

        self.assertTrue(time_mock.called)
        logJson = json.loads(self.buffer.getvalue())
        self.assertEqual(logJson.get("timestamp"), "2017-07-14T02:40:00+00:00")

    def testJsonCustomDefault(self):
        def custom(o):
            return "very custom"
        fr = jsonlogger.JsonFormatter(json_default=custom)
        self.logHandler.setFormatter(fr)

        msg = {"adate": datetime.datetime(1999, 12, 31, 23, 59),
               "normal": "value"}
        self.logger.info(msg)
        logJson = json.loads(self.buffer.getvalue())
        self.assertEqual(logJson.get("adate"), "very custom")
        self.assertEqual(logJson.get("normal"), "value")

    def testJsonCustomLogicAddsField(self):
        class CustomJsonFormatter(jsonlogger.JsonFormatter):

            def process_log_record(self, log_record):
                log_record["custom"] = "value"
                # Old Style "super" since Python 2.6's logging.Formatter is old
                # style
                return jsonlogger.JsonFormatter.process_log_record(self, log_record)

        self.logHandler.setFormatter(CustomJsonFormatter())
        self.logger.info("message")
        logJson = json.loads(self.buffer.getvalue())
        self.assertEqual(logJson.get("custom"), "value")

    def testExcInfo(self):
        fr = jsonlogger.JsonFormatter()
        self.logHandler.setFormatter(fr)
        try:
            raise Exception('test')
        except Exception:

            self.logger.exception("hello")

            expected_value = traceback.format_exc()
            # Formatter removes trailing new line
            if expected_value.endswith('\n'):
                expected_value = expected_value[:-1]

        logJson = json.loads(self.buffer.getvalue())
        self.assertEqual(logJson.get("exc_info"), expected_value)

    def testEnsureAsciiTrue(self):
        fr = jsonlogger.JsonFormatter()
        self.logHandler.setFormatter(fr)
        self.logger.info('Привет')
        msg = self.buffer.getvalue().split('"message": "', 1)[1].split('"', 1)[0]
        self.assertEqual(msg, r"\u041f\u0440\u0438\u0432\u0435\u0442")

    def testEnsureAsciiFalse(self):
        fr = jsonlogger.JsonFormatter(json_ensure_ascii=False)
        self.logHandler.setFormatter(fr)
        self.logger.info('Привет')
        msg = self.buffer.getvalue().split('"message": "', 1)[1].split('"', 1)[0]
        self.assertEqual(msg, "Привет")

    def testCustomObjectSerialization(self):
        def encode_complex(z):
            if isinstance(z, complex):
                return (z.real, z.imag)
            else:
                type_name = z.__class__.__name__
                raise TypeError("Object of type '{}' is no JSON serializable".format(type_name))

        formatter = jsonlogger.JsonFormatter(json_default=encode_complex,
                                             json_encoder=json.JSONEncoder)
        self.logHandler.setFormatter(formatter)

        value = {
            "special": complex(3, 8),
        }

        self.logger.info(" message", extra=value)
        msg = self.buffer.getvalue()
        self.assertEqual(msg, "{\"message\": \" message\", \"special\": [3.0, 8.0]}\n")

if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        if sys.argv[1] == 'xml':
            testSuite = unittest.TestLoader().loadTestsFromTestCase(
                TestJsonLogger)
            xmlrunner.XMLTestRunner(output='reports').run(testSuite)
    else:
        unittest.main()
