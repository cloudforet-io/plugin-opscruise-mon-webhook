import logging
import unittest
import os
import json
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json
from pprint import pprint

_LOGGER = logging.getLogger(__name__)


class TestEvent(TestCase):
    def test_parse(self):
        params = {
            "options": {},
            "data": {
                "text": "",
                "disable_notification": "false"
            }
        }
        parsed_data = self.monitoring.Event.parse(params)
        print(parsed_data)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
