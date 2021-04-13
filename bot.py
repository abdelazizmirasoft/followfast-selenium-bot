from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
import re
import math
import io
import datetime
from selenium.webdriver.chrome.options import Options

username = ""
password = ""


def loadDriver():
    options = webdriver.ChromeOptions()
    # To ignore the check of the SSL Certificate
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # To download automatically files
    options.add_experimental_option("prefs", {
        "download.default_directory": r"c:\XML",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(executable_path=ChromeDriverManager(
    ).install(), options=options)

    driver.get('https://followfast.com/login.php')
    return driver


def login(driver):
    # 1: Username
    driver.find_element_by_name('username').send_keys(username)
    # 2: Password
    driver.find_element_by_name('pass').send_keys(password)
    # Some time to type the captcha
    time.sleep(5)
    # 3: Submit button
    driver.find_element_by_name('login').click()


def doFbSubs():
    global driver
    driver.find_element_by_css_selector("a[href*='fbsubs.php'] ").click()


def doTasks():
    time.sleep(10)
    doFbSubs()


if __name__ == "__main__":
    try:
        driver = loadDriver()
        login(driver)
        while True:
            doTasks()

    except:
        print("Re-try")
        driver.quit()
