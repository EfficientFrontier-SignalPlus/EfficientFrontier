from core.protocol import EFProtocol
from core.sp_api import SPApi
from loguru import logger


async def forward(strategy_secret, synapse: EFProtocol) -> EFProtocol:
    logger.info(f"miner forward()")
    # try:
    #     validator_uid = synapse.input['validator_uid']
    # except Exception as e:
    #     logger.error(f"get validator uid error: {e}")
    #     validator_uid = -1
    validator_uid = synapse.input.get('validator_uid', -1)
    sp_api = SPApi(strategy_secret)
    try:
        report_data = sp_api.get_report_data(validator_uid)
    except Exception as e:
        logger.error(f"get report data error: {e}")
        report_data = {}
    synapse.output = report_data
    logger.info(f'my strategy data: {report_data}')
    return synapse
