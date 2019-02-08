import json
import os
import urllib.request
from typing import List, Iterable
from urllib.error import HTTPError

from bs4 import BeautifulSoup

from src.config import html_dir, headers
from src.logger import Logger

local_dir = "../data/"


class TargetElement:
    def __init__(self, json_filename: str):
        with open(json_filename, mode="r") as file:
            file_dict = json.load(file)

        self.name = file_dict["name"]
        self.url = file_dict["url"]
        self.tag = file_dict["tag"]
        self.attribute_selections = file_dict.get("attribute_selections", dict())
        self.attribute_exceptions = file_dict.get("attribute_exceptions", dict())
        self.text_selections = file_dict.get("text_selections", set())
        self.text_exceptions = file_dict.get("text_exceptions", set())


def get_html_targets() -> List[TargetElement]:
    targets = []
    for filename in os.listdir(html_dir):
        if not filename.endswith(".json"):
            continue
        full_path = os.path.join(html_dir, filename)
        each_target = TargetElement(full_path)
        if any(each_target.name == _t.name for _t in targets):
            Logger.log("Double name {:s} in file {:s}.".format(each_target.name, filename))
            continue
        targets.append(each_target)
    return targets


def update_state_html(targets: Iterable[TargetElement]) -> List[str]:
    text = []
    if not os.path.isdir(local_dir):
        os.makedirs(local_dir)

    tmp_file_path = local_dir + "html_state.json"
    if os.path.isfile(tmp_file_path):
        with open(tmp_file_path, mode="r") as file:
            temp_storage = json.load(file)
    else:
        Logger.log("Initializing temp html storage.")
        temp_storage = dict()

    for target_element in targets:
        Logger.log("Polling {:s}...".format(target_element.name))
        request = urllib.request.Request(target_element.url, data=None, headers=headers)

        try:
            page = urllib.request.urlopen(request)
            html = page.read()
            soup = BeautifulSoup(html, "html.parser")

            result_elements = []
            for each_selection_key, all_selection_values in target_element.attribute_selections.items():
                for each_selection_value in all_selection_values:
                    try:
                        for each_exception_key, all_exception_values in target_element.attribute_exceptions.items():
                            for each_exception_value in all_exception_values:
                                exceptions = soup.find(target_element.tag, {each_exception_key: each_exception_value})
                                if exceptions is not None:
                                    exceptions.extract()

                        found = soup.find_all(target_element.tag, {each_selection_key: each_selection_value})
                        if found is None:
                            Logger.log("URL {:s} not responsive for tag {:s} and selection {:s}={:s}".format(target_element.url, target_element.tag, each_selection_key, each_selection_value))
                            continue

                        selected = []
                        for each_element in found:
                            if 0 >= len(target_element.text_selections):
                                selected.append(each_element)
                                continue

                            text = each_element.get_text("\n", strip=True)
                            for each_text_selection in target_element.text_selections:
                                if each_text_selection in text:
                                    selected.append(each_element)

                        for each_element in selected:
                            for each_text_exception in target_element.text_exceptions:
                                if each_text_exception in text:
                                    break
                            else:
                                result_elements.append(each_element)

                    except HTTPError:
                        Logger.log("Problem polling {:s} with tag {:s} and selection {:s}={:s}.".format(target_element.url, target_element.tag, each_selection_key, each_selection_value))

            contained_texts = [each_result.get_text("\n", strip=True) for each_result in result_elements]
            hash_values = {hash(each_text): each_text for each_text in contained_texts}
            last_hash_values = temp_storage.get(target_element.name)
            if last_hash_values is None:
                Logger.log("Initializing {:s} with {:d} entries...".format(target_element.name, len(hash_values)))

            else:
                for each_new_hash, each_content in hash_values.items():
                    if each_new_hash in last_hash_values:
                        continue
                    Logger.log("New entry for {:s}".format(target_element.name))
                    message = "<a href={:s}>{:s}</a>\n{:s}\n".format(target_element.url, target_element.name, each_content)
                    text.append(message)

            temp_storage[target_element.name] = sorted(hash_values.keys())

        except HTTPError:
            Logger.log("Target {} unresponsive.".format(target_element.name))

    with open(tmp_file_path, mode="w") as file:
        json.dump(temp_storage, file, indent=2, sort_keys=True)

    return text
