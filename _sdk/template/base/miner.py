import time
import asyncio
import threading
import argparse
import traceback

import bittensor as bt

from _sdk.template.base.neuron import BaseNeuron
from _sdk.template.utils.config import add_miner_args

from typing import Union
from loguru import logger

class BaseMinerNeuron(BaseNeuron):
    """
    Base class for Bittensor miners.
    """

    neuron_type: str = "MinerNeuron"

    @classmethod
    def add_args(cls, parser: argparse.ArgumentParser):
        # Adding command-line arguments specific to the miner.
        super().add_args(parser)
        add_miner_args(cls, parser)

    def __init__(self, config=None):
        super().__init__(config=config)

        # Issue warning if allowing anyone to send requests.
        if not self.config.blacklist.force_validator_permit:
            logger.warning("You are allowing non-validators to send requests to your miner. This is a security risk.")
        if self.config.blacklist.allow_non_registered:
            logger.warning("You are allowing unregistered entities to send requests to your miner. This is a security risk.")

        # Axon handles requests, allowing validators to send requests to the miner.
        self.axon = bt.axon(wallet=self.wallet, config=self.config() if callable(self.config) else self.config, port=self.config.axon.port)

        # Attach the function to be called when servicing requests.
        logger.info("Attaching forward function to the miner's axon.")
        self.axon.attach(forward_fn=self.forward, blacklist_fn=self.blacklist, priority_fn=self.priority)
        logger.info(f"Axon creation complete: {self.axon}")

        # Instantiate runner.
        self.should_exit: bool = False
        self.is_running: bool = False
        self.thread: Union[threading.Thread, None] = None
        self.lock = asyncio.Lock()

    def save_state(self):
        # Placeholder for saving miner state, can be implemented as needed.
        return

    def run(self):
        """
        Main loop to start and manage the miner on the Bittensor network. Handles graceful shutdown and logs unexpected errors.

        Main Tasks:
        1. Check if registered on the Bittensor network.
        2. Start the miner's axon and make it active on the network.
        3. Periodically resync with the chain; update metagraph and set weights.

        The miner continues running until `should_exit` is set to True or an external interrupt occurs.
        During each operation cycle, the miner waits for a new block on the Bittensor network, updates its network knowledge (metagraph), and sets weights.

        Exceptions:
            KeyboardInterrupt: If the miner is manually interrupted.
            Exception: Unexpected errors during miner operation are logged for diagnostics.
        """

        # Check if the miner is registered on the network.
        self.sync()

        # Serve axon information to the network + netuid.
        logger.info(f"Serving miner axon {self.axon} on network {self.config.subtensor.chain_endpoint}, netuid: {self.config.netuid}")
        self.axon.serve(netuid=self.config.netuid, subtensor=self.subtensor)

        # Start the miner's axon and make it active on the network.
        self.axon.start()
        logger.info(f"Miner started at block {self.block}")

        # Keep the miner operational until intentionally stopped.
        try:
            while not self.should_exit:
                # Wait until epoch length is reached before updating metagraph.
                while self.block - self.metagraph.last_update[self.uid] < self.config.neuron.epoch_length:
                    # logger.info(f'self.block: {self.block}, '
                    #                 f'self.metagraph.last_update[self.uid]: {self.metagraph.last_update[self.uid]}, '
                    #                 f'Difference: {self.block - self.metagraph.last_update[self.uid]}, '
                    #                 f'self.config.neuron.epoch_length: {self.config.neuron.epoch_length}')
                    # Wait before checking again.
                    time.sleep(10)

                    # Check if miner should exit.
                    if self.should_exit:
                        break

                # Sync metagraph and possibly set weights.
                self.sync()
                self.step += 1
                time.sleep(10)

        # Handle manual stop of miner for safe termination.
        except KeyboardInterrupt:
            self.axon.stop()
            logger.info("Miner terminated by keyboard interrupt.")
            exit()

        # Handle unexpected errors by logging and continuing operation.
        except Exception as e:
            logger.error(traceback.format_exc())

    def run_in_background_thread(self):
        """
        Start miner operation in a separate background thread.
        Useful for non-blocking operation.
        """
        if not self.is_running:
            logger.debug("Starting miner in background thread.")
            self.should_exit = False
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            self.is_running = True
            logger.debug("Miner started.")

    def stop_run_thread(self):
        """
        Stop the miner operation running in the background thread.
        """
        if self.is_running:
            logger.debug("Stopping miner in background thread.")
            self.should_exit = True
            if self.thread is not None:
                self.thread.join(5)
            self.is_running = False
            logger.debug("Miner stopped.")

    def __enter__(self):
        """
        Start miner operation in a background thread when entering context.
        This method facilitates the use of the miner with a 'with' statement.
        """
        self.run_in_background_thread()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Stop the miner's background operation when exiting context.
        This method facilitates the use of the miner with a 'with' statement.

        Args:
            exc_type: Type of the exception that caused the context to exit. None if exiting without exception.
            exc_value: Exception instance that caused the context to exit. None if exiting without exception.
            traceback: Traceback object encoding the stack trace. None if exiting without exception.
        """
        self.stop_run_thread()

    def resync_metagraph(self):
        """
        Resync the metagraph and update hotkeys and moving averages based on the new metagraph.
        """
        # Import copy to make a deepcopy of the previous metagraph.
        import copy
        previous_metagraph = copy.deepcopy(self.metagraph)

        # Sync the metagraph.
        self.metagraph.sync(subtensor=self.subtensor)

        # Check if the metagraph axon info has changed.
        if previous_metagraph.axons == self.metagraph.axons:
            # If metagraph hasn't changed, wait before next check.
            time.sleep(1)
            return
        time.sleep(1)