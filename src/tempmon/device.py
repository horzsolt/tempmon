import logging
from bluepy import btle
from retry import retry
from notification_handler import DataCaptureDelegate
from sink import Sink


class TemperatureMonitor():

    def __init__(self, sink: Sink, mac: str, device_id: str) -> None:
        self._logger = logging.getLogger(__name__)
        self._connected = False
        self._sink = sink
        self._mac = mac
        self._device_id = device_id
        self._device = None

    @retry(btle.BTLEDisconnectError, delay=10, tries=20)
    def connect(self) -> None:
        self._logger.info(f"Connecting to {self._device_id} ")
        try:
            self._device = btle.Peripheral(self._mac)
            self._connected = True
            self._device.setDelegate(DataCaptureDelegate(self._sink, self._device_id))
            self._logger.debug(f"Connection done {self._device_id}")
        except btle.BTLEDisconnectError as error:
            self._logger.error(f"Connecting to device {self._device_id} failed. Retrying...")
            self._logger.error(error, exc_info=False)
            raise

    def receive_metrics(self) -> None:
        try:
            if self._connected:
                self._logger.debug(f"Waiting for data for {self._device_id}")
                result = self._device.waitForNotifications(15)

                if (not result):
                    self._logger.debug(f"Receiving data from device {self._device_id} has timed out.")
            else:
                self._logger.debug(f"Device {self._device_id} is not connected, can't receive metrics.")
        except Exception as ex:
            self._logger.error(f"Device {self._device_id} failed to receive data.")
            self._logger.error(ex, exc_info=False)

    def disconnect(self) -> None:
        if self._connected:
            self._device.disconnect()
            self._logger.debug(f"Device {self._device_id} disconnected.")
