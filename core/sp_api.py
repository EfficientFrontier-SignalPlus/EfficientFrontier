import json
import random
from loguru import logger
import requests
from enum import Enum

from core.env_setting.env_utils import get_env_setting
from core.ranking_model import ScoreModel
from core.utils import verify256


class Endpoint(Enum):
    GET_REPORT_DATA = ('GET', '/api/mining/bittensor-proxy/miner-report-data')


class SPApi:
    strategy_secret = None

    def __init__(self, strategy_secret: str):
        self.domain = get_env_setting().sp_api_domain
        self.strategy_secret = strategy_secret

    def get_report_data(self, validator_uid, validator_version, validator_git_hash) -> dict:
        logger.info(f'get report data, validator_uid: {validator_uid}, validator_version: {validator_version}, '
                    f'validator_git_hash: {validator_git_hash}')
        url = self.domain + Endpoint.GET_REPORT_DATA.value[1]
        body = {"strategySecret": self.strategy_secret,
                "validatorVersion": validator_version,
                "validatorUid": validator_uid}
        headers = {"Trace-Id": str(random.randint(100000, 999999))}
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            logger.info(f'headers: {headers}, data: {data}')
            if data['code'] != 0:
                raise Exception(f"Request failed, {Endpoint.GET_REPORT_DATA}, error message: {data['message']}")
            r = verify256(data['value']['rawData'], data['value']['signature'])
            if not r:
                raise Exception('signature verify failed')
            data_str = data.get('value').get('rawData')
            data_json = json.loads(data_str)
            return data_json
        else:
            logger.debug(
                f'{self.strategy_secret[:8]}***{self.strategy_secret[-8:]} get report data failed, status code: {response.status_code}')
            response.raise_for_status()

            return {}


class ReportDataHandler:
    @staticmethod
    def create_score_model(data: dict) -> ScoreModel:
        return ScoreModel(**data)


if __name__ == '__main__':
    sp_api = SPApi('4082eb5d-61f1-48aa-b563-10291648b5ff')
    report_data = sp_api.get_report_data('1', '1')
    score_model = ReportDataHandler.create_score_model(report_data)
    print(score_model.score)
