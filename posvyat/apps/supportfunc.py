import json
import os

from loguru import logger

CONFIG_FILE_PATH = '/config/'


def read_json_choices(file_path: str) -> list:
    # create_folder(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE_PATH)
    print(os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE_PATH))
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__)) + CONFIG_FILE_PATH):
        for filename in files:
            if (filename == file_path):
                logger.info(f'Reading file - {filename}')
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as file:
                    return list(json.load(file).items())
    return []


def check_phone(phone: str) -> int:
    response = read_json_choices("phones.json")
    if (len(response) > 0):
        if (phone in response[0][1]):
            return 1
        else:
            return 0
    else:
        return -1
