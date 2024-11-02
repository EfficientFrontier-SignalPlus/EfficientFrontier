from multiprocessing import Process
import time
from loguru import logger
from core.utils import read_timestamp, write_timestamp, remove_timestamp_file
from _sdk.neurons.validator import Validator


def foo():
    with Validator() as validator:
        while True:
            time.sleep(60)


if __name__ == "__main__":

    def start_foo():
        p = Process(target=foo)
        p.start()
        return p


    # Initialize the timestamp file with current time
    write_timestamp(time.time())

    p = start_foo()

    try:
        while True:
            timestamp = read_timestamp()
            if timestamp is not None:
                now = time.time()
                elapsed = round(now - timestamp,0)
                logger.info(f"Main process checking timestamp: {timestamp}, elapsed: {elapsed} seconds")
                timeout_min = 30
                if elapsed > timeout_min * 60:
                    logger.info(f"Main process timestamp not updated in over {timeout_min} minutes. Restarting...")
                    p.terminate()
                    p.join()
                    # Reset timestamp
                    write_timestamp(time.time())
                    p = start_foo()
            else:
                logger.info("Failed to read timestamp")
            time.sleep(60)  # Check every 10 seconds
    except KeyboardInterrupt:
        logger.info("Exiting...")
        p.terminate()
        p.join()
        remove_timestamp_file()
