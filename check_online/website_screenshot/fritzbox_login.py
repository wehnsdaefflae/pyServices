import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# https://dzone.com/articles/taking-browser-screenshots-no
# $ sudo apt-get install python-pip xvfb xserver-xephyr
# $ sudo pip install selenium
from pyvirtualdisplay import Display

with open("fritz_pw.json", mode="r") as file:
    config = json.load(file)

password = config["password"]
driver_path = config["driver_path"]

display = Display(visible=0, size=(800, 800))
display.start()

# options = webdriver.FirefoxOptions()
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument('disable-infobars')

# https://github.com/mozilla/geckodriver/releases
# browser = webdriver.Firefox(executable_path=driver_path)
browser = webdriver.Chrome(executable_path=driver_path)

browser.get("http://fritz.box/?sid=8e06fe6c834e1533&lp=dslSpec")

WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input#uiPass"))).send_keys(password)
browser.find_element_by_css_selector("button#submitLoginBtn").click()

WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "form#main_form")))
screen_shot = browser.save_screenshot("my_screenshot.png")

browser.quit()
display.stop()
