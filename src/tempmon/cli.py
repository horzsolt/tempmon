from device import TemperatureMonitor
from pg_sink import PostgresSink
import logging

def run():
    logging.basicConfig(filename="app.log", level=logging.DEBUG)
    with (PostgresSink()) as sink:
        tm = TemperatureMonitor(sink)
        try:
            tm.connect()
            tm.receive_metrics()
        finally:
            tm.disconnect()

if __name__ == "__main__":
    run()
