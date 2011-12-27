import unittest, sys, logging
from StringIO import StringIO

sys.path += ['../src']
import jsonlogger

class testJsonLogger(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.buffer = StringIO()
        
        self.logHandler = logging.StreamHandler(self.buffer)
        self.logger.addHandler(self.logHandler)

    def testJSONOutput(self):
        fr = jsonlogger.JsonFormatter()
        self.logHandler.setFormatter(fr)

        self.logger.info("testing stream")

        self.assertEqual(self.buffer.getvalue(), '{"message": "testing stream"}\n')

if __name__=='__main__':
    unittest.main()
