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

import traceback
import numpy as np
from core.env_setting.env_utils import get_env_setting
from core.protocol import EFProtocol
from core.utils import get_current_commit_hash, read_latest_success_set_weights_datetime_str
from bittensor import logging


async def forward(validator):
    """
    https://docs.learnbittensor.org/resources/glossary#recycling-and-burning

    Burn 100% of the miner’s emissions.
    """
    owner_uid = 161
    try:
        await validator.dendrite(
            axons=[validator.metagraph.axons[uid] for uid in [owner_uid]],
            synapse=EFProtocol(input={'validator_uid': validator.uid,
                                      'validator_version': get_env_setting().validator_version,
                                      'validator_git_hash': get_current_commit_hash()[:7],
                                      'last_set_weights_success_time': read_latest_success_set_weights_datetime_str()
                                      }),
            deserialize=True,
        )
    except Exception:
        logging.error(traceback.format_exc())

    validator.update_scores(np.array([1.0]), [owner_uid])
