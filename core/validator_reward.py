# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 <your name>

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
        score_model = ReportDataHandler.create_score_model(response)
        score = score_model.score
        logger.info(f"In reward end, miner_uid:{miner_uid}, score: {score}")
        return score
    except Exception as e:
        logger.error(f"Error in rewards: {e}, miner data: {response}")
        return None


def get_rewards(query: int, responses: list, miner_uids: list) -> np.ndarray:
    return np.array(
        [reward(query, response, miner_uid) for response, miner_uid in zip(responses, miner_uids)], dtype=float
    )
