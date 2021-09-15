import base64
import json
import os


def get_settings(config):
    settings = {}
    for field_name, field_value in config.__dict__.items():
        if field_name.isupper():
            settings[field_name] = field_value
    return settings


def load_json_from_file(json_file_location):
    with open(json_file_location, "r") as file:
        return json.load(file)


def load_json_from_env(env_name):
    return json.loads(base64.b64decode(os.getenv(env_name)))
