import time

from selenium import webdriver


def login(name, password):
    pass

DRIVER = "D:/Eigene Dateien/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(DRIVER)
driver.get("http://fritz.box/?sid=8e06fe6c834e1533&lp=dslSpec")
time.sleep(10)
screen_shot = driver.save_screenshot("my_screenshot.png")
driver.quit()
