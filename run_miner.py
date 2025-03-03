from _sdk.neurons.miner import Miner
import time
import os
from loguru import logger
from core.miner_forward import get_last_update_time

if __name__ == "__main__":
    with Miner() as miner:
        while True:
            current_time = time.time()
            last_update_time = get_last_update_time()
            time_since_update = current_time - last_update_time
            
            if time_since_update > 3600:  # 3600 seconds = 1 hour
                logger.error(f"No data updates for more than 1 hour. Last update time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_update_time))}. Forcing exit.")
                os._exit(0)
            else:
                logger.info(f"Miner running... Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}, Last update: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_update_time))}, Time since last update: {time_since_update/60:.2f} minutes")
            time.sleep(60)
