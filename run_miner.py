from _sdk.neurons.miner import Miner
import bittensor as bt
import time
from loguru import logger

if __name__ == "__main__":
    with Miner() as miner:
        while True:
            logger.info(f"Miner running... {time.time()}")
            time.sleep(60)
