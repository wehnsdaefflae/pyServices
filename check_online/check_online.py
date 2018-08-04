#!/usr/bin/env python3

import datetime
import json
import os
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def check_online(host, port):
    with socket(AF_INET, SOCK_STREAM) as s:     # Creates socket
        try:
            s.connect((host, port))             # tries to connect to the host

        except Exception as e:                  # if failed to connect
            return False

    return True


def save_spectrum(file_path):
    # https://dzone.com/articles/taking-browser-screenshots-no
    # $ sudo apt-get install python-pip xvfb xserver-xephyr chromium-chromedriver
    # $ sudo pip install selenium

    with open("fritz_pw.json", mode="r") as file:
        config = json.load(file)

    password = config["password"]
    driver_path = config["driver_path"]

    display = Display(visible=0, size=(800, 800))
    display.start()

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')

    # https://github.com/mozilla/geckodriver/releases
    browser = webdriver.Chrome(executable_path=driver_path)

    browser.get("http://fritz.box/?sid=8e06fe6c834e1533&lp=dslSpec")

    WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input#uiPass"))).send_keys(password)
    browser.find_element_by_css_selector("button#submitLoginBtn").click()

    WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "form#main_form")))
    screen_shot = browser.save_screenshot(file_path)

    browser.quit()
    display.stop()


def make_screenshot(file_name):
    dir_path = "screenshots/"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    save_spectrum(dir_path + file_name)


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

            make_screenshot(offline_start.strftime("%Y-%m-%d_%H:%M:%S") + ".png")

        elif offline_start is not None and is_online:
            now = datetime.datetime.now()
            print("{:s}: online".format(now.strftime("%Y-%m-%d %H:%M:%S")))
            span = now - offline_start

            if 10 < span.seconds:
                row = [offline_start.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")]
                with open(file_path, mode="a") as file:
                    file.write("\t".join(row) + "\n")

                make_screenshot(offline_start.strftime("%Y-%m-%d_%H:%M:%S") + ".png")

            offline_start = None

        time.sleep(5)


if __name__ == "__main__":
    main()
