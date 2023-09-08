from tempmon.device import TemperatureMonitor
from tempmon.pg_sink import PostgresSink

def run():
    with (PostgresSink()) as sink:
        tm = TemperatureMonitor(sink)
        tm.receive_metrics()
