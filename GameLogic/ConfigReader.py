import json
import os


class ConfigReader:

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def get_rules_from_config(file_name):
        file_path = os.path.join(ConfigReader.CURRENT_DIR, file_name)
        with open(file_path) as file:
            contents = file.read()
            as_json = json.loads(contents)
            print(as_json)
        return as_json

