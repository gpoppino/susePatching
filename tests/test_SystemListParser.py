import unittest
from susePatching import SystemListParser

class TestSystemListParser(unittest.TestCase):

    def setUp(self):
        self.parser = SystemListParser("not-used-filename")

    def testSystemListParser(self):
        self.assertDictEqual({}, self.parser.getSystems())

        self.parser._addSystem("instance-k3s-1.suse.local,2022-10-07 17:45:00")
        self.assertDictEqual({"2022-10-07 17:45:00" : ["instance-k3s-1.suse.local"]}, self.parser.getSystems())

        self.parser._addSystem("instance-k3s-2.suse.local,2022-10-08 17:50:00")
        self.assertDictEqual({"2022-10-07 17:45:00" : ["instance-k3s-1.suse.local"], "2022-10-08 17:50:00": ["instance-k3s-2.suse.local"]}, self.parser.getSystems())

        self.parser._addSystem("instance-k3s-3.suse.local,2022-10-07 17:45:00")
        self.assertDictEqual({"2022-10-07 17:45:00" : ["instance-k3s-1.suse.local", "instance-k3s-3.suse.local"], "2022-10-08 17:50:00" : ["instance-k3s-2.suse.local"]}, self.parser.getSystems())