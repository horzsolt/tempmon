import logging
import json
from sink import Sink
from metric import Metric
from mailer import sendMail

class TemperatureMonitor():

    def __init__(self, sink: Sink) -> None:
        self._logger = logging.getLogger(__name__)
        self._connected = False
        self._sink = sink

    def receive_metrics(self, client, userdata, msg) -> None:
            # {"time":"2023-11-11 12:39:09","model":"Nexus-TH","id":45,"channel":1,"battery_ok":1,"temperature_C":22.9,"humidity":61}
            self._logger.debug(f"Received {msg.payload.decode()} from {msg.topic} topic")

            try:
                _json = json.loads(msg.payload.decode())
                metric = Metric(float(_json["temperature_C"]), float(
                    _json["humidity"]), float(_json["battery_ok"]), int(_json["id"]), int(_json["channel"]))
                self._logger.debug(f"Callback received with {metric}")
                self._sink.store_metric(metric)
            except Exception as ex:
                self._logger.error(ex, exc_info=True)
                sendMail(ex)
