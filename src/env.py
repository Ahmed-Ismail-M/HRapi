import os
import json

def get_env(file_name:str, default_setting: dict, directory:str)->dict:
    path = f"{directory}\\{file_name}"
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as setting:
            json.dump(default_setting , setting, ensure_ascii=False, indent=4)
            return default_setting
    else:
        with open(path, 'r', encoding='utf-8') as setting:
            return json.load(setting)