import base64
import os
import subprocess

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

from core.env_setting.env_utils import get_env_setting


def verify256(data: str, sign: str) -> bool:
    encoded_key = base64.b64decode(get_env_setting().public_key_pem)
    public_key = serialization.load_der_public_key(encoded_key)
    try:
        signature = base64.b64decode(sign)
        public_key.verify(
            signature,
            data.encode('utf-8'),
            padding=padding.PKCS1v15(),
            algorithm=hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


timestamp_file = 'timestamp.txt'


def write_timestamp(current_time):
    tmp_file = timestamp_file + '.tmp'
    with open(tmp_file, 'w') as f:
        f.write(str(current_time))
    os.replace(tmp_file, timestamp_file)  # Atomic operation to replace the file


def read_timestamp():
    try:
        with open(timestamp_file, 'r') as f:
            timestamp_str = f.read()
            return float(timestamp_str)
    except (FileNotFoundError, ValueError):
        return None


def remove_timestamp_file():
    if os.path.exists(timestamp_file):
        os.remove(timestamp_file)


def get_current_commit_hash():
    try:
        commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        return commit_hash
    except Exception as e:
        return "unknown"


if __name__ == '__main__':
    r = verify256('test', 'test')
    print(r)
