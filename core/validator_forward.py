# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
import json
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

import time
import bittensor as bt
from bittensor import logging

from core.env_setting.env_utils import get_env_setting
from core.protocol import EFProtocol
from core.utils import get_current_commit_hash, read_latest_success_set_weights_datetime_str
from core.validator_reward import get_rewards
from _sdk.template.utils.uids import get_random_uids
from loguru import logger


async def forward(validator):
    num_uids = 256
    batch_size = 5
    miner_uids = get_random_uids(validator, k=num_uids)
    logger.info(f"forward miner uids: {miner_uids}")

    all_responses = []
    for i in range(0, num_uids, batch_size):
        batch_uids = miner_uids[i:i + batch_size]

        # for miner_uid in batch_uids:
        #     axon = self.metagraph.axons[miner_uid]
        #     logger.info(f"miner_uid: {miner_uid}, {axon.ip}:{axon.port}")

        responses = await validator.dendrite(
            axons=[validator.metagraph.axons[uid] for uid in batch_uids],
            synapse=EFProtocol(input={'validator_uid': validator.uid,
                                      'validator_version': get_env_setting().validator_version,
                                      'validator_git_hash': get_current_commit_hash()[:7],
                                      'last_set_weights_success_time': read_latest_success_set_weights_datetime_str()
                                      }),
            deserialize=True,
        )

        all_responses.extend(responses)

    rewards = get_rewards(query=validator.step, responses=all_responses, miner_uids=list(miner_uids))
    assert len(miner_uids) == len(all_responses) == len(rewards)

    for idx, (uid, response, reward) in enumerate(zip(miner_uids, all_responses, rewards)):
        try:
            logger.info(f"uid: {uid}, coldkey:{validator.metagraph.axons[uid].coldkey[:10]}, "
                        f"response: {response}, reward: {rewards[idx]}")
        except Exception as e:
            logger.error(f"Error in logging: {e}")
    log_str = '\n'
    total_reward = sum(rewards)
    if total_reward != 0:
        for uid, response, reward in zip(miner_uids, all_responses, rewards):
            try:
                if reward != 0:
                    try:
                        raw_date = json.loads(response.get('value').get('rawData'))
                    except Exception as e:
                        logger.warning(f'Error in parsing raw data(uid {uid}): {e}, response: {response}')
                        continue
                    reward_percentage = (reward / total_reward) * 100
                    log_str += (f"uid: {uid}, coldkey: {validator.metagraph.axons[uid].coldkey[:4]}, "
                                f"strategyId: {raw_date.get('strategyId')[-4:]}, "
                                f"reward: {reward:.4f}, "
                                f"percentage: {reward_percentage:.2f}%, total_reward: {round(total_reward,2)}\n")
            except Exception as e:
                logger.error(f"Error in logging: {e}, uid: {uid}, response: {response}, reward: {reward}")
        logger.info(log_str)
    validator.update_scores(rewards, miner_uids)
