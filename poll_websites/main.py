import time
import datetime
import traceback
from typing import Callable

import unidecode

from src.check_files import get_file_targets, update_state_files
from src.check_html import update_state_html, get_html_targets
from src.config import receiver
from src.logger import Logger, time_format
from src.sendMessage import send_gmail


def check_for_changes():
    targets_html = get_html_targets()
    targets_file = get_file_targets()

    result = update_state_html(targets_html) + update_state_files(targets_file)

    if 0 < len(result):
        text = "\n".join(result)
        send_gmail([receiver], "[Website-Veränderung!]", unidecode.unidecode(text), debug=False)


def repeat_indefinitely(function: Callable[[], None], minutes_interval: int):
    last_second = -1

    while True:
        now = datetime.datetime.now()
        this_minute = now.minute

        while this_minute % minutes_interval != 0 or this_minute == last_second:
            Logger.log("{:s}: waiting".format(now.strftime(time_format)))
            time.sleep(10)
            now = datetime.datetime.now()
            this_minute = now.minute

        last_second = this_minute

        Logger.log("{:s}: executing function".format(now.strftime(time_format)))

        # noinspection PyBroadException
        try:
            function()

        except Exception as e:
            Logger.log(traceback.format_exc())
            continue


def main():
    repeat_indefinitely(check_for_changes, 5)


if __name__ == "__main__":
    main()
