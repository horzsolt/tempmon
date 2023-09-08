import logging
from typing import Self
from bluepy import btle
from retry import retry
from .notification_handler import DataCaptureDelegate
from .sink import Sink

logger = logging.getLogger(__name__)

class TemperatureMonitor():

    mac = "A4:C1:38:85:EC:F1"
    connected = False
    device = None

    def __init__(self, sink: Sink) -> None:
        self.connected = False
        self._sink = sink

    @retry(btle.BTLEDisconnectError, delay=2, tries=2)
    def connect(self) -> None:
        logger.info(f"Connecting to {self.mac}")
        try:
            self.device = btle.Peripheral(self.mac)
            self.connected = True
            logger.debug("Connection done...")
        except btle.BTLEDisconnectError as error:
            logger.error(error, exc_info=True)

    def receive_metrics(self) -> None:
        try:
            if self.connected:
                self.device.setDelegate(DataCaptureDelegate(self._sink))
                logger.debug("Waiting for data...")
                self.device.waitForNotifications(15.0)
        except Exception as ex:
            logger.error(ex, exc_info=True)

    def disconnect(self) -> None:
        if self.connected:
            self.device.disconnect()
