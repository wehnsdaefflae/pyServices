#!/usr/bin/env python3

import datetime
import os
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM


def check_online(host, port):
    with socket(AF_INET, SOCK_STREAM) as s:     # Creates socket
        try:
            s.connect((host, port))             # tries to connect to the host

        except Exception as e:                  # if failed to connect
            return False

    return True


def main():
    args = sys.argv
    if len(args) < 4:
        print("requires arguments: host port target_file")
        exit()

    host = args[1]       # "google.de"
    port = args[2]       # 443
    file_path = args[3]  # "online_record.csv"
    if not os.path.isfile(file_path):
        header = ["offline_start", "offline_end"]
        with open(file_path, mode="w") as file:
            file.write("\t".join(header) + "\n")

    offline_start = None
    while True:
        is_online = check_online(host, int(port))

        if offline_start is None and not is_online:
            offline_start = datetime.datetime.now()
            print("{:s}: offline".format(offline_start.strftime("%Y-%m-%d %H:%M:%S")))

        elif offline_start is not None and is_online:
            now = datetime.datetime.now()
            print("{:s}: online".format(now.strftime("%Y-%m-%d %H:%M:%S")))
            span = now - offline_start

            if 10 < span.seconds:
                row = [offline_start.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")]

                with open(file_path, mode="a") as file:
                    file.write("\t".join(row) + "\n")

            offline_start = None

        time.sleep(5)


if __name__ == "__main__":
    main()
