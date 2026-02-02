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

import json
import time
import bittensor as bt
import numpy as np
from bittensor import logging

from core.env_setting.env_utils import get_env_setting
from core.protocol import EFProtocol
from core.utils import get_current_commit_hash, read_latest_success_set_weights_datetime_str
from core.validator_reward import get_rewards
from _sdk.template.utils.uids import get_random_uids
from loguru import logger


async def forward(validator):
    num_uids = 256
    batch_size = 20
    miner_uids = get_random_uids(validator, k=num_uids)
    logger.info(f"forward miner uids:\n{miner_uids}")

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

    try:
        total_reward = sum(rewards)
        if total_reward != 0:
            data_list = []
            for uid, response, reward in zip(miner_uids, all_responses, rewards):
                if reward == 0:
                    continue
                try:
                    raw_data_str = response.get('value', {}).get('rawData', '{}')
                    raw_data = json.loads(raw_data_str)
                    reward_percentage = (reward / total_reward) * 100

                    data_list.append({
                        'uid': uid,
                        'coldkey': validator.metagraph.axons[uid].coldkey[:4],
                        'strategy_id': (raw_data.get('strategyId') or '')[-4:],
                        'reward': reward,
                        'reward_percentage': reward_percentage
                    })
                except Exception as e:
                    logger.warning(
                        f'Error parsing rawData (uid={uid}): {e}, response: {response}'
                    )

            log_lines = []
            for item in data_list:
                log_lines.append(
                    f"uid: {item['uid']}, coldkey: {item['coldkey']}, "
                    f"strategyId: {item['strategy_id']}, "
                    f"reward: {item['reward']:.4f}, "
                    f"percentage: {item['reward_percentage']:.2f}%, "
                    f"total_reward: {round(total_reward, 2)}"
                )

            log_lines.append(f"count of non-zero rewards: {len(data_list)}")
            log_lines.append("reward sorted:")

            data_list_sorted = sorted(data_list, key=lambda x: x['reward'], reverse=True)
            for item in data_list_sorted:
                log_lines.append(
                    f"uid: {item['uid']}, coldkey: {item['coldkey']}, "
                    f"strategyId: {item['strategy_id']}, "
                    f"reward: {item['reward']:.4f}, "
                    f"percentage: {item['reward_percentage']:.2f}%, "
                    f"total_reward: {round(total_reward, 2)}"
                )

            log_str = "\n".join(log_lines)
            logger.info("\n" + log_str)
    except Exception as e:
        logger.error(f"Error in logging: {e}")
    """
        https://docs.learnbittensor.org/resources/glossary#recycling-and-burning

        Burn 100% of the miner’s emissions.
    """
    owner_uid = 161
    validator.update_scores(np.array([1.0]), [owner_uid])
