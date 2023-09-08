import time
import unittest
from unittest.mock import Mock

from src.tempmon.device import TemperatureMonitor

class Testing(unittest.TestCase):

    def test_receive_metrics_more_than_once(self):
        mock = Mock()
        tm = TemperatureMonitor(mock)
        try:
            tm.connect()
            tm.receive_metrics()
            time.sleep(1)
            tm.receive_metrics()
            time.sleep(1)
            tm.receive_metrics()
        finally:
            tm.disconnect()
        self.assertEqual(mock.store_metric.call_count, 3)


