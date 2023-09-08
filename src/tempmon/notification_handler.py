import logging
from bluepy import btle
from metric import Metric
from sink import Sink

logger = logging.getLogger(__name__)

class DataCaptureDelegate(btle.DefaultDelegate):

    def __init__(self, sink: Sink) -> None:
        btle.DefaultDelegate.__init__(self)
        self._sink = sink

    def handleNotification(self, cHandle, data) -> None:
        databytes = bytearray(data)
        temperature = int.from_bytes(databytes[0:2],"little") / 100
        humidity = int.from_bytes(databytes[2:3],"little")
        battery = int.from_bytes(databytes[3:5],"little") / 1000
        metric = Metric(temperature, humidity, battery)
        self._sink.store_metric(metric)
        logger.debug(metric)