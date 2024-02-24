import logging
import json
from sink import Sink
from metric import Metric
from button import Button
from mailer import sendMail

class DeviceMonitor():

    def __init__(self, sink: Sink) -> None:
        self._logger = logging.getLogger(__name__)
        self._connected = False
        self._sink = sink

    def receive_metrics(self, client, userdata, msg: str) -> None:
            # {"time":"2023-11-11 12:39:09","model":"Nexus-TH","id":45,"channel":1,"battery_ok":1,"temperature_C":22.9,"humidity":61}
            # {'time': '2023-11-12 12:42:29', 'model': 'Microchip-HCS200', 'id': '0A8651EA', 'id_rev': '578A6150', 'encrypted': '0004D920', 'encrypted_rev': '049B2000', 'button1': 'ON', 'button2': 'OFF', 'button3': 'OFF', 'button4': 'OFF', 'misc': '', 'battery_ok': 0}
            self._logger.debug(f"Received {msg.payload.decode()} from {msg.topic} topic")

            try:
                _json = json.loads(msg.payload.decode())
                _temperature = None
                _humidity = None
                _continue = True

                if (_json):

                    if (_json.get("model", "")) == "Microchip-HCS200":
                        id = _json.get("id", "")
                        button1 = _json.get("button1", "")
                        button2 = _json.get("button2", "")
                        button3 = _json.get("button3", "")
                        button4 = _json.get("button4", "")
                        battery = _json.get("battery_ok", "")
                        misc = _json.get("misc", "")

                        button = Button(id, button1, button2, button3, button4, battery, misc)
                        self._sink.store_button(button)

                    elif (_json.get("model", "")) == "Nexus-TH":
                        if (_json.get("temperature_C", "")) != "":
                            _temperature = _json["temperature_C"]
                        else:
                            _continue = False

                        if (_json.get("humidity", "")) != "":
                            _humidity = _json["humidity"]
                        else:
                            _continue = False

                        if (_continue):
                            metric = Metric(float(_temperature), float(
                                _humidity), float(_json["battery_ok"]), int(_json["id"]), int(_json["channel"]))
                            self._logger.debug(f"Callback received with {metric}")
                            self._sink.store_metric(metric)
                    else:
                        self._logger.error(f"Callback received with invalid JSON {_json}")
                else:
                     self._logger.error("Callback received with empty JSON")
            except Exception as ex:
                self._logger.error(ex, exc_info=True)
                sendMail(ex)
