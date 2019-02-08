import json
import os
from typing import List, Iterable

import requests

from poll_websites.src.config import file_dir, headers
from poll_websites.src.logger import Logger

local_dir = "../data/"


class TargetFile:
    def __init__(self, filename: str):
        raise NotImplementedError()
        basename = os.path.basename(filename)
        self.name = os.path.splitext(basename)[0]

        with open(filename, mode="r") as file:
            line = file.readline()
            self.url = line.strip()


def get_file_targets() -> List[TargetFile]:
    targets = []
    for filename in os.listdir(file_dir):
        if filename.endswith(".json"):
            full_path = os.path.join(file_dir, filename)
            targets.append(TargetFile(full_path))
    return targets


def update_state_files(targets: Iterable[TargetFile]) -> List[str]:
    text = []
    tmp_file_path = local_dir + "file_state.json"
    if os.path.isfile(tmp_file_path):
        with open(tmp_file_path, mode="r") as file:
            temp_storage = json.load(file)
    else:
        Logger.log(f"Initializing temp file storage.")
        temp_storage = dict()

    for target_file in targets:
        Logger.log(f"Polling {target_file.url:s}...")
        response = requests.get(target_file.url, headers=headers)
        size = len(response.content)

        last_size = temp_storage.get(target_file.name)
        if last_size is None:
            Logger.log(f"Initializing {target_file.name:s}...")

        elif not last_size == size:
            text.append(target_file.url)

        temp_storage[target_file.name] = size

    with open(tmp_file_path, mode="w") as file:
        json.dump(temp_storage, file, indent=2, sort_keys=True)

    return text
