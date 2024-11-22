from core.protocol import EFProtocol
from core.sp_api import SPApi
from loguru import logger


async def forward(strategy_secret, synapse: EFProtocol) -> EFProtocol:
    logger.info(f"miner forward()")
    validator_uid = synapse.input.get('validator_uid', -1)
    validator_version = synapse.input.get('validator_version', '0.0.0')
    sp_api = SPApi(strategy_secret)
    try:
        report_data = sp_api.get_report_data(validator_uid,validator_version)
    except Exception as e:
        logger.error(f"get report data error: {e}")
        report_data = {}
    synapse.output = report_data
    logger.info(f'my strategy data: {report_data}')
    return synapse
