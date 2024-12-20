# The MIT License (MIT)
# Copyright © 2023 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import copy

import bittensor as bt
import bittensor_wallet as bw
from abc import ABC, abstractmethod

# from dev_tools.new_wallet import hotkey
# Sync calls set weights and also resyncs the metagraph.
from _sdk.template.utils.config import check_config, add_args, config
from _sdk.template.utils.misc import ttl_get_block
from _sdk.template import __spec_version__ as spec_version
from loguru import logger


# from template.mock import MockSubtensor, MockMetagraph


class BaseNeuron(ABC):
    """
    Base class for Bittensor miners. This class is abstract and should be inherited by a subclass. It contains the core logic for all neurons; validators and miners.

    In addition to creating a wallet, subtensor, and metagraph, this class also handles the synchronization of the network state via a basic checkpointing mechanism based on epoch length.
    """

    neuron_type: str = "BaseNeuron"

    @classmethod
    def check_config(cls, config: "bt.Config"):
        check_config(cls, config)

    @classmethod
    def add_args(cls, parser):
        add_args(cls, parser)

    @classmethod
    def config(cls):
        return config(cls)

    subtensor: "bt.subtensor"
    wallet: "bt.wallet"
    metagraph: "bt.metagraph"
    spec_version: int = spec_version

    @property
    def block(self):
        return ttl_get_block(self)

    def __init__(self, config=None):
        base_config = copy.deepcopy(config or BaseNeuron.config())
        self.config = self.config()
        self.config.merge(base_config)
        # self.check_config(self.config)

        # Set up logging with the provided configuration.
        # bt.logging.set_config(config=self.config.logging)

        # If a gpu is required, set the device to cuda:N (e.g. cuda:0)
        self.device = self.config.neuron.device

        # Log the configuration for reference.
        logger.info(self.config)

        # Build Bittensor objects
        # These are core Bittensor classes to interact with the network.
        logger.info("Setting up bittensor objects.")

        # The wallet holds the cryptographic key pairs for the miner.
        # if self.config.mock:
        #     self.wallet = bt.MockWallet(config=self.config)
        #     self.subtensor = MockSubtensor(
        #         self.config.netuid, wallet=self.wallet
        #     )
        #     self.metagraph = MockMetagraph(
        #         self.config.netuid, subtensor=self.subtensor
        #     )
        # else:
        #     self.wallet = bt.wallet(config=self.config)
        #     self.subtensor = bt.subtensor(config=self.config)
        #     self.metagraph = self.subtensor.metagraph(self.config.netuid)

        self.wallet = bw.Wallet(name=self.config.wallet.name, hotkey=self.config.wallet.hotkey)
        bw.config.wallet = self.wallet
        self.subtensor = bt.subtensor(config=self.config)
        self.metagraph = self.subtensor.metagraph(self.config.netuid)

        logger.info(f"Wallet: {self.wallet}")
        logger.info(f"Subtensor: {self.subtensor}")
        logger.info(f"Metagraph: {self.metagraph}")

        # Check if the miner is registered on the Bittensor network before proceeding further.
        self.check_registered()

        # Each miner gets a unique identity (UID) in the network for differentiation.
        self.uid = self.metagraph.hotkeys.index(
            self.wallet.hotkey.ss58_address
        )
        logger.info(
            f"Running neuron on subnet: {self.config.netuid} with uid {self.uid} using network: {self.subtensor.chain_endpoint}"
        )
        self.step = 0

    @abstractmethod
    async def forward(self, synapse: bt.Synapse) -> bt.Synapse:
        ...

    @abstractmethod
    def run(self):
        ...

    def sync(self):
        """
        Wrapper for synchronizing the state of the network for the given miner or validator.
        """
        # Ensure miner or validator hotkey is still registered on the network.
        self.check_registered()
        if self.should_sync_metagraph():
            self.resync_metagraph()

        if self.should_set_weights():
            self.set_weights()

        # Always save state.
        self.save_state()

    def check_registered(self):
        # --- Check for registration.
        if not self.subtensor.is_hotkey_registered(
                netuid=self.config.netuid,
                hotkey_ss58=self.wallet.hotkey.ss58_address,
        ):
            logger.error(
                f"Wallet: {self.wallet} is not registered on netuid {self.config.netuid}."
                f" Please register the hotkey using `btcli subnets register` before trying again"
            )
            exit()

    def should_sync_metagraph(self):
        """
        Check if enough epoch blocks have elapsed since the last checkpoint to sync.
        """
        last_update = self.metagraph.last_update[self.uid]
        diff = self.block - last_update
        epoch_length = self.config.neuron.epoch_length
        # logger.info(f'self.uid, {self.uid}, should_sync_metagraph, '
        #                 f'self.block: {self.block} - last_update: {last_update} = {diff} need > epoch_length {epoch_length}, last_update: {self.metagraph.last_update}')
        return (self.block - last_update) > epoch_length

    def should_set_weights(self) -> bool:
        # Don't set weights on initialization.
        if self.step == 0:
            logger.info(f"should_set_weights(): Skipping set weights on initialization.")
            return False

        # Check if enough epoch blocks have elapsed since the last epoch.
        if self.config.neuron.disable_set_weights:
            logger.info(f"should_set_weights(): Skipping set weights due to disable_set_weights.")
            return False

        # Define appropriate logic for when set weights.
        if self.neuron_type == "MinerNeuron":
            return False

        if (self.block - self.metagraph.last_update[self.uid]) > self.config.neuron.epoch_length:
            logger.info(f"should_set_weights(): Setting weights for {self.neuron_type} at block {self.block}")
            return True
        else:
            logger.info(f'should_set_weights(): Waiting for Block: {self.block} - last_update: {self.metagraph.last_update[self.uid]} = '
                        f'{(self.block - self.metagraph.last_update[self.uid])}, '
                        f'which needs to exceed epoch_length of {self.config.neuron.epoch_length}.')
            return False

    def save_state(self):
        logger.warning(
            "save_state() not implemented for this neuron. You can implement this function to save model checkpoints or other useful data."
        )

    def load_state(self):
        logger.warning(
            "load_state() not implemented for this neuron. You can implement this function to load model checkpoints or other useful data."
        )
