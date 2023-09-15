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
        params = {"options": {},
                  "data": {
                      "anomaly": {
                          "model": "RE",
                          "propertyClass": "Threshold"
                      },
                      "description": "Azure vm:ecommerce-vm-02 cpu utilization(92.18) is high for the past 1m",
                      "header": {
                          "action": "CREATE",
                          "msgSubType": "New",
                          "msgType": "Open",
                          "retrieved": "2023-08-30T18:32:47.243Z",
                          "version": "0.1"
                      },
                      "summary": "Azure vm:ecommerce-vm-02 cpu utilization(92.18) is high",
                      "target": {
                          "app": "UNKNOWN",
                          "cid": "dev",
                          "displaLevel": "High",
                          "name": "test-01",
                          "resourceGroup": "NETWORK",
                          "saas": "",
                          "subscription": "xxxxxx-xxxxxxx-xxxxxxx",
                          "targetContainer": "",
                          "targetNamespace": "NETWORK",
                          "targetNode": "",
                          "targetPod": "",
                          "type": "Instance",
                          "vid": "12345678901234567"
                      },
                      "tenant": {
                          "locale": "en_US",
                          "realmName": "",
                          "tenantId": "dev",
                          "tenantName": "dev-TEST"
                      },
                      "ticket": {
                          "created": "2023-08-30T18:29:38.453Z",
                          "displayId": "1234",
                          "escalation": "Critical",
                          "priority": "High",
                          "ticketId": "123f0a67-4567-89dd-aa12-b34a56de7890",
                          "type": "Anomaly",
                          "updated": "2023-08-30T18:32:39.140Z",
                          "url": "https://test.com"
                      }
                  }}
        parsed_data = self.monitoring.Event.parse(params)
        print(parsed_data)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
