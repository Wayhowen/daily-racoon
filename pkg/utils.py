import base64
import json
import os


def get_settings(config):
    settings = {}
    for field_name, field_value in config.__dict__.items():
        if field_name.isupper():
            settings[field_name] = field_value
    return settings


def load_json_from_file(json_file_location) -> dict:
    with open(json_file_location, "r") as file:
        return json.load(file)


def load_json_from_env(env_name: str) -> dict:
    return json.loads(os.getenv(env_name))


def load_from_env(env_name: str) -> str:
    return os.getenv(env_name)


def decode_base64(encoded_string: str) -> str:
    return base64.b64decode(encoded_string)
