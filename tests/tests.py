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

from io import StringIO

sys.path.append('src/python-json-logger')
from pythonjsonlogger import jsonlogger
import datetime


class TestJsonLogger(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("logging-test-{}".format(random.randint(1, 101)))
        self.log.setLevel(logging.DEBUG)
        self.buffer = StringIO()

        self.log_handler = logging.StreamHandler(self.buffer)
        self.log.addHandler(self.log_handler)

    def test_default_format(self):
        fr = jsonlogger.JsonFormatter()
        self.log_handler.setFormatter(fr)

        msg = "testing logging format"
        self.log.info(msg)
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["message"], msg)

    def test_percentage_format(self):
        fr = jsonlogger.JsonFormatter(
            # All kind of different styles to check the regex
            '[%(levelname)8s] %(message)s %(filename)s:%(lineno)d %(asctime)'
        )
        self.log_handler.setFormatter(fr)

        msg = "testing logging format"
        self.log.info(msg)
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["message"], msg)
        self.assertEqual(log_json.keys(), {'levelname', 'message', 'filename', 'lineno', 'asctime'})

    def test_rename_base_field(self):
        fr = jsonlogger.JsonFormatter(rename_fields={'message': '@message'})
        self.log_handler.setFormatter(fr)

        msg = "testing logging format"
        self.log.info(msg)
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["@message"], msg)

    def test_rename_nonexistent_field(self):
        fr = jsonlogger.JsonFormatter(rename_fields={'nonexistent_key': 'new_name'})
        self.log_handler.setFormatter(fr)

        stderr_watcher = StringIO()
        sys.stderr = stderr_watcher
        self.log.info("testing logging rename")

        self.assertTrue("KeyError: 'nonexistent_key'" in stderr_watcher.getvalue())

    def test_add_static_fields(self):
        fr = jsonlogger.JsonFormatter(static_fields={'log_stream': 'kafka'})

        self.log_handler.setFormatter(fr)

        msg = "testing static fields"
        self.log.info(msg)
        log_json = json.loads(self.buffer.getvalue())

        self.assertEqual(log_json["log_stream"], "kafka")
        self.assertEqual(log_json["message"], msg)

    def test_format_keys(self):
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
        self.log_handler.setFormatter(fr)

        msg = "testing logging format"
        self.log.info(msg)
        log_msg = self.buffer.getvalue()
        log_json = json.loads(log_msg)

        for supported_key in supported_keys:
            if supported_key in log_json:
                self.assertTrue(True)

    def test_unknown_format_key(self):
        fr = jsonlogger.JsonFormatter('%(unknown_key)s %(message)s')

        self.log_handler.setFormatter(fr)
        msg = "testing unknown logging format"
        try:
            self.log.info(msg)
        except Exception:
            self.assertTrue(False, "Should succeed")

    def test_log_adict(self):
        fr = jsonlogger.JsonFormatter()
        self.log_handler.setFormatter(fr)

        msg = {"text": "testing logging", "num": 1, 5: "9",
               "nested": {"more": "data"}}

        self.log.info(msg)
        log_json = json.loads(self.buffer.getvalue())
        self.assertEqual(log_json.get("text"), msg["text"])
        self.assertEqual(log_json.get("num"), msg["num"])
        self.assertEqual(log_json.get("5"), msg[5])
        self.assertEqual(log_json.get("nested"), msg["nested"])
        self.assertEqual(log_json["message"], "")

    def test_log_extra(self):
        fr = jsonlogger.JsonFormatter()
        self.log_handler.setFormatter(fr)

        extra = {"text": "testing logging", "num": 1, 5: "9",
                 "nested": {"more": "data"}}
        self.log.info("hello", extra=extra)
        log_json = json.loads(self.buffer.getvalue())
        self.assertEqual(log_json.get("text"), extra["text"])
        self.assertEqual(log_json.get("num"), extra["num"])
        self.assertEqual(log_json.get("5"), extra[5])
        self.assertEqual(log_json.get("nested"), extra["nested"])
        self.assertEqual(log_json["message"], "hello")

    def test_json_default_encoder(self):
        fr = jsonlogger.JsonFormatter()
        self.log_handler.setFormatter(fr)

        msg = {"adate": datetime.datetime(1999, 12, 31, 23, 59),
               "otherdate": datetime.date(1789, 7, 14),
               "otherdatetime": datetime.datetime(1789, 7, 14, 23, 59),
               "otherdatetimeagain": datetime.datetime(1900, 1, 1)}
        self.log.info(msg)
        log_json = json.loads(self.buffer.getvalue())
        self.assertEqual(log_json.get("adate"), "1999-12-31T23:59:00")
        self.assertEqual(log_json.get("otherdate"), "1789-07-14")
        self.assertEqual(log_json.get("otherdatetime"), "1789-07-14T23:59:00")
        self.assertEqual(log_json.get("otherdatetimeagain"),
                         "1900-01-01T00:00:00")

    @unittest.mock.patch('time.time', return_value=1500000000.0)
    def test_json_default_encoder_with_timestamp(self, time_mock):
        fr = jsonlogger.JsonFormatter(timestamp=True)
        self.log_handler.setFormatter(fr)

        self.log.info("Hello")

        self.assertTrue(time_mock.called)
        log_json = json.loads(self.buffer.getvalue())
        self.assertEqual(log_json.get("timestamp"), "2017-07-14T02:40:00+00:00")

    def test_json_custom_default(self):
        def custom(o):
            return "very custom"
        fr = jsonlogger.JsonFormatter(json_default=custom)
        self.log_handler.setFormatter(fr)

        msg = {"adate": datetime.datetime(1999, 12, 31, 23, 59),
               "normal": "value"}
        self.log.info(msg)
        log_json = json.loads(self.buffer.getvalue())
        self.assertEqual(log_json.get("adate"), "very custom")
        self.assertEqual(log_json.get("normal"), "value")

    def test_json_custom_logic_adds_field(self):
        class CustomJsonFormatter(jsonlogger.JsonFormatter):

            def process_log_record(self, log_record):
                log_record["custom"] = "value"
                # Old Style "super" since Python 2.6's logging.Formatter is old
                # style
                return jsonlogger.JsonFormatter.process_log_record(self, log_record)

        self.log_handler.setFormatter(CustomJsonFormatter())
        self.log.info("message")
        log_json = json.loads(self.buffer.getvalue())
        self.assertEqual(log_json.get("custom"), "value")

    def get_traceback_from_exception_followed_by_log_call(self) -> str:
        try:
            raise Exception('test')
        except Exception:
            self.log.exception("hello")
            str_traceback = traceback.format_exc()
            # Formatter removes trailing new line
            if str_traceback.endswith('\n'):
                str_traceback = str_traceback[:-1]

        return str_traceback

    def test_exc_info(self):
        fr = jsonlogger.JsonFormatter()
        self.log_handler.setFormatter(fr)
        expected_value = self.get_traceback_from_exception_followed_by_log_call()

        log_json = json.loads(self.buffer.getvalue())
        self.assertEqual(log_json.get("exc_info"), expected_value)

    def test_exc_info_renamed(self):
        fr = jsonlogger.JsonFormatter("%(exc_info)s", rename_fields={"exc_info": "stack_trace"})
        self.log_handler.setFormatter(fr)
        expected_value = self.get_traceback_from_exception_followed_by_log_call()

        log_json = json.loads(self.buffer.getvalue())
        self.assertEqual(log_json.get("stack_trace"), expected_value)
        self.assertEqual(log_json.get("exc_info"), None)

    def test_ensure_ascii_true(self):
        fr = jsonlogger.JsonFormatter()
        self.log_handler.setFormatter(fr)
        self.log.info('Привет')
        msg = self.buffer.getvalue().split('"message": "', 1)[1].split('"', 1)[0]
        self.assertEqual(msg, r"\u041f\u0440\u0438\u0432\u0435\u0442")

    def test_ensure_ascii_false(self):
        fr = jsonlogger.JsonFormatter(json_ensure_ascii=False)
        self.log_handler.setFormatter(fr)
        self.log.info('Привет')
        msg = self.buffer.getvalue().split('"message": "', 1)[1].split('"', 1)[0]
        self.assertEqual(msg, "Привет")

    def test_custom_object_serialization(self):
        def encode_complex(z):
            if isinstance(z, complex):
                return (z.real, z.imag)
            else:
                type_name = z.__class__.__name__
                raise TypeError("Object of type '{}' is no JSON serializable".format(type_name))

        formatter = jsonlogger.JsonFormatter(json_default=encode_complex,
                                             json_encoder=json.JSONEncoder)
        self.log_handler.setFormatter(formatter)

        value = {
            "special": complex(3, 8),
        }

        self.log.info(" message", extra=value)
        msg = self.buffer.getvalue()
        self.assertEqual(msg, "{\"message\": \" message\", \"special\": [3.0, 8.0]}\n")

    def test_rename_reserved_attrs(self):
        log_format = lambda x: ['%({0:s})s'.format(i) for i in x]
        reserved_attrs_map = {
            'exc_info': 'error.type',
            'exc_text': 'error.message',
            'funcName': 'log.origin.function',
            'levelname': 'log.level',
            'module': 'log.origin.file.name',
            'processName': 'process.name',
            'threadName': 'process.thread.name',
            'msg': 'log.message'
        }

        custom_format = ' '.join(log_format(reserved_attrs_map.keys()))
        reserved_attrs = [_ for _ in jsonlogger.RESERVED_ATTRS if _ not in list(reserved_attrs_map.keys())]
        formatter = jsonlogger.JsonFormatter(custom_format, reserved_attrs=reserved_attrs, rename_fields=reserved_attrs_map)
        self.log_handler.setFormatter(formatter)
        self.log.info("message")

        msg = self.buffer.getvalue()
        self.assertEqual(msg, '{"error.type": null, "error.message": null, "log.origin.function": "test_rename_reserved_attrs", "log.level": "INFO", "log.origin.file.name": "tests", "process.name": "MainProcess", "process.thread.name": "MainThread", "log.message": "message"}\n')

    def test_merge_record_extra(self):
        record = logging.LogRecord("name", level=1, pathname="", lineno=1, msg="Some message", args=None, exc_info=None)
        output = jsonlogger.merge_record_extra(record, target=dict(foo="bar"), reserved=[])
        self.assertIn("foo", output)
        self.assertIn("msg", output)
        self.assertEquals(output["foo"], "bar")
        self.assertEquals(output["msg"], "Some message")


if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        if sys.argv[1] == 'xml':
            testSuite = unittest.TestLoader().loadTestsFromTestCase(
                TestJsonLogger)
            xmlrunner.XMLTestRunner(output='reports').run(testSuite)
    else:
        unittest.main()
