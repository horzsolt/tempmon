import logging
import psycopg2
import os
from configparser import ConfigParser
from datetime import datetime, timezone
from button import Button
from mailer import sendMail

from metric import Metric
from sink import Sink

logger = logging.getLogger(__name__)

class PostgresSink(Sink):

    def __init__(self) -> None:

        config_object = ConfigParser()
        config_object.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.ini"))
        serverinfo = config_object["CONFIG"]

        self.host = serverinfo["POSTGRES_HOST"]
        self.user = serverinfo["POSTGRES_USER"]
        self.pwd = serverinfo["POSTGRES_PWD"]
        self.database = serverinfo["POSTGRES_DATABASE"]
        self.schema = serverinfo["POSTGRES_SCHEMA"]
        self.conn = None

        logger.debug(f"host {self.host}")
        logger.debug(f"user {self.user}")

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, type, value, traceback) -> None:
        self._disconnect()

    def _disconnect(self) -> None:
        if (self.conn != None):
            self.conn.close()

    def _connect(self) -> None:
        logger.debug("connect to pg")
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                port=2665,
                database=self.database
            )
        except Exception as ex:
            logger.error(ex, exc_info=True)

    def store_metric(self, metric: Metric) -> None:

        insert_command = f'''INSERT INTO {self.schema}.conditions (time, device_id, temperature, humidity, battery, channel)
         VALUES('{datetime.now(timezone.utc)}', '{metric.device_id}', '{metric.temperature}', '{metric.humidity}'
        , '{metric.battery}', '{metric.channel}');'''

        try:
            logger.debug(f"store_record {insert_command}")
            cursor = self.conn.cursor()
            cursor.execute(insert_command)
            self.conn.commit()
        except Exception as ex:
            logger.error(ex, exc_info=True)
            sendMail(ex.message)

    def store_button(self, button: Button) -> None:

        insert_command = f'''INSERT INTO {self.schema}.buttons (time, device_id, button1, button2, button3, button4, battery, misc)
         VALUES('{datetime.now(timezone.utc)}', '{button.device_id}', '{button.button1}', '{button.button2}', '{button.button3}', '{button.button4}'
        , '{button.battery}', '{button.misc}');'''

        try:
            logger.debug(f"store_record {insert_command}")
            cursor = self.conn.cursor()
            cursor.execute(insert_command)
            self.conn.commit()
        except Exception as ex:
            logger.error(ex, exc_info=True)
            sendMail(ex.message)
