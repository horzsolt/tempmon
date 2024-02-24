import paho.mqtt.client as mqtt
import logging
import os
from device import DeviceMonitor
from pg_sink import PostgresSink
from configparser import ConfigParser
from mailer import sendMail

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.debug("Connected to MQTT Broker!")
    else:
        logger.debug("Failed to connect, return code %d\n", rc)

def run():

    with (PostgresSink()) as sink:
        tm = DeviceMonitor(sink)
        try:
            sendMail("Starting the loop")
            logger.debug("Starting the loop.")

            client = mqtt.Client('temperature monitor')

            config_object = ConfigParser()
            config_object.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.ini"))
            serverinfo = config_object["CONFIG"]
            mqtt_host = serverinfo["MQTT_HOST"]
            username = serverinfo["MQTT_USER"]
            password = serverinfo["MQTT_PWD"]

            client.username_pw_set(username, password)
            client.on_connect = on_connect
            client.connect(mqtt_host, 1883)
            client.subscribe('rtl_433')
            client.on_message = tm.receive_metrics

            client.loop_forever()

        finally:
            logger.debug("Finishing and disconnecting.")
            sendMail("Finishing and disconnecting.")

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    filename="tempmon.log",
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    run()
