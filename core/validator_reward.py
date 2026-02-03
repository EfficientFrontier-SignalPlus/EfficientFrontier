# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 <your name>
import time
import traceback

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
import numpy as np
import json
from loguru import logger
from core.sp_api import ReportDataHandler
from core.utils import verify256
import bittensor as bt

sub = bt.subtensor(network='finney')


class MetaGraphCache:
    def __init__(self, netuid, ttl=600):
        self.netuid = netuid
        self.ttl = ttl
        self._m = None
        self._last_update = 0

    def get_metagraph(self):
        if time.time() - self._last_update > self.ttl or self._m is None:
            if self._m is None:
                self._m = sub.metagraph(netuid=self.netuid)
            self._m.sync(subtensor=sub)
            self._last_update = time.time()
        return self._m


cache = MetaGraphCache(netuid=53)


def get_coldkey_hotkey_by_uid(miner_uid):
    m = cache.get_metagraph()
    return m.coldkeys[miner_uid], m.hotkeys[miner_uid]


def is_measure_time_expired(measure_time):
    return (time.time() - measure_time / 1000) / 3600 > 25


def reward(query: int, response: dict, miner_uid: int) -> float:
    """
    Reward the miner response to the dummy request. This method returns a reward
    value for the miner, which is used to update the miner's score.

    Returns:
    - float: The reward value for the miner.
    """
    try:
        logger.info(f"In reward start, miner_uid:{miner_uid}, query val: {query}, miner's data': {response}")
        if response == {}:
            return 0

        r = verify256(response['value']['rawData'], response['value']['signature'])
        if not r:
            logger.error(f"verify256 failed, miner_uid:{miner_uid}, response: {response}")
            return 0
        data_str = response.get('value').get('rawData')
        data_json = json.loads(data_str)

        score_model = ReportDataHandler.create_score_model(data_json)

        miner_coldkey, miner_hotkey = get_coldkey_hotkey_by_uid(miner_uid)
        if miner_hotkey != score_model.hotkey or miner_coldkey != score_model.coldkey:
            logger.warning(
                f"Miner hotkey or coldkey mismatch, miner_hotkey: {miner_hotkey}, miner_uid: {miner_uid}, "
                f"score_model.hotkey: {score_model.hotkey}, score_model.coldkey: {score_model.coldkey}")
            return 0

        if is_measure_time_expired(score_model.measureTime):
            logger.warning(
                f"Miner data is too old, miner_uid: {miner_uid}, score_model.measureTime: {score_model.measureTime}")
            return 0

        score = score_model.score
        logger.info(f"In reward end, miner_uid:{miner_uid}, score: {score}")
        return score
    except Exception as e:
        logger.error(f"Error in rewards: {e},{traceback.format_exc()}, miner data: {response}")
        return 0


def get_rewards(query: int, responses: list, miner_uids: list) -> np.ndarray:
    return np.array(
        [reward(query, response, miner_uid) for response, miner_uid in zip(responses, miner_uids)], dtype=float
    )
