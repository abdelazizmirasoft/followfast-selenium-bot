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
    # 4: Username
    driver.find_element_by_name('username').send_keys(username)
    # open_select_ministry = driver.find_element_by_xpath(
    #     '//center/table/tbody/tr/td[1]/div/div[2]/div/div/table/tbody/tr/').send_keys("Adm1nRNC$2015")

    # 5: Password
    driver.find_element_by_name('pass').send_keys(password)
    # open_select_ministry = driver.find_element_by_xpath(
    #     '//tbody/tr[8]/td[1]/input').send_keys("Adm1nRNC$2015")
    time.sleep(3)
    # 6: Submit button
    driver.find_element_by_name('login').click()


if __name__ == "__main__":
    try:
        driver = loadDriver()
        login(driver)
        time.sleep(10)

    except:
        print("Re-try")
        driver.quit()
