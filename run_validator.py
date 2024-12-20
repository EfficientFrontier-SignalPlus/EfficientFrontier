from multiprocessing import Process
import time
from loguru import logger
from core.utils import read_latest_success_set_weights_timestamp, write_latest_success_set_weights_timestamp, remove_timestamp_file
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
    write_latest_success_set_weights_timestamp(time.time())

    p = start_foo()

    try:
        while True:
            timestamp = read_latest_success_set_weights_timestamp()
            if timestamp is not None:
                now = time.time()
                elapsed = round(now - timestamp, 0)
                logger.info(f"Main process checking timestamp: {timestamp}, elapsed: {elapsed} seconds")
                timeout_min = 50
                if elapsed > timeout_min * 60:
                    logger.info(f"Main process timestamp not updated in over {timeout_min} minutes. Restarting...")
                    p.terminate()
                    p.join()
                    # Reset timestamp
                    write_latest_success_set_weights_timestamp(time.time())
                    p = start_foo()
            else:
                logger.info("Failed to read timestamp")
            time.sleep(60 * 5)  # Check every 10 seconds
    except KeyboardInterrupt:
        logger.info("Exiting...")
        p.terminate()
        p.join()
        remove_timestamp_file()
