from ..device import TemperatureMonitor
from ..pg_sink import PostgresSink

def run():
    with (PostgresSink()) as sink:
        tm = TemperatureMonitor(sink)
        tm.receive_metrics()
