import logging
from bluepy import btle
from metric import Metric
from sink import Sink


class DataCaptureDelegate(btle.DefaultDelegate):

    def __init__(self, sink: Sink, device_id=1) -> None:

        self._logger = logging.getLogger(__name__)
        self._sink = sink
        self._device_id = device_id
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data) -> None:
        databytes = bytearray(data)
        temperature = int.from_bytes(databytes[0:2],"little") / 100
        humidity = int.from_bytes(databytes[2:3],"little")
        battery = int.from_bytes(databytes[3:5],"little") / 1000
        metric = Metric(temperature, humidity, battery, self._device_id)
        self._sink.store_metric(metric)
        self._logger.debug(f"Callback received with {metric}")