import time
from device import TemperatureMonitor
from pg_sink import PostgresSink
import logging
from threading import Thread

def task(device_id : str, mac : str) -> None:

    logger = logging.getLogger(__name__)
    logger.debug(f"Starting task for {device_id}, {mac}")

    with (PostgresSink()) as sink:
        tm = TemperatureMonitor(sink, mac, device_id)
        try:
            tm.connect()
            logger.debug(f"{device_id} starting the loop.")

            while True:
                time.sleep(10)
                tm.receive_metrics()
        finally:
            logger.debug(f"{device_id} finishing and disconnecting.")
            tm.disconnect()

def run():

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        filename="app.log",
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    #threadLock = threading.Lock()
    threads = []
    devices = ("A4:C1:38:85:EC:F1", "A4:C1:38:49:9A:89")

    for x in devices:
        t = Thread(target=task, args=(str(x+1), devices[x]))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    run()
