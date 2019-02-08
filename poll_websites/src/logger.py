# coding=utf-8
import datetime


time_format = "%Y-%m-%d %H:%M:%S"


class Logger:
    target_file = ""

    @staticmethod
    def log(text: str):
        now = datetime.datetime.now()
        if 0 < len(Logger.target_file):
            with open(Logger.target_file, mode="a") as file:
                file.write(f"{now.strftime(time_format):s}:\t{text:s}\n")
        print(text)
