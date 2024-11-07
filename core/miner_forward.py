import bittensor as bt
from core.protocol import EFProtocol
from core.sp_api import SPApi
from loguru import logger

async def forward(strategy_secret, synapse: EFProtocol) -> EFProtocol:
    logger.info(f"miner forward()")
    sp_api = SPApi(strategy_secret)
    logger.info(f'debug 11')
    report_data = sp_api.get_report_data()
    logger.info(f'debug 12')
    synapse.output = report_data
    logger.info(f'debug 13')
    logger.info(f'my strategy data: {report_data}')
    return synapse
