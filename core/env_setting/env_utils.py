import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--env", type=str, help="running environment", required=True)
args, _ = parser.parse_known_args()
env = args.env


def get_env_setting():
    if env in ['prod']:
        from core.env_setting import setting_prod as env_setting
    elif env == 'dev':
        from core.env_setting import setting_dev as env_setting
    elif env == 'test':
        from core.env_setting import setting_test as env_setting
    else:
        print(f'Configuration error, please check! env={env}')
        os._exit(0)
    return env_setting.Env
