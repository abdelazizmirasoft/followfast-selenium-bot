from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import re
import math
import io
import datetime
from random import randint
from selenium.webdriver.chrome.options import Options

username = ""
password = ""

twitterUser = ""
twitterPwd = ""


def loadDriver():
    options = webdriver.ChromeOptions()
    # To ignore the check of the SSL Certificate
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(executable_path=ChromeDriverManager(
    ).install(), options=options)
    driver.get('https://followfast.com/login.php')
    return driver


# This function is to close all tabs other than 0 from 1 to n
def closeTabs(n):
    global driver
    # Loop tabs
    for i in range(1, n+1):
        window_name = driver.window_handles[i]
        driver.switch_to.window(window_name=window_name)
        driver.close()
    # Switch back to the main tab
    window_name = driver.window_handles[0]
    driver.switch_to.window(window_name=window_name)

# This function is to move to the tab n


def moveToTab(n):
    global driver
    # Switch back to the main tab
    window_name = driver.window_handles[n]
    driver.switch_to.window(window_name=window_name)


# Login to Twitter
def loginTwitter():
    global driver
    print('Twitter')
    # Open a new window
    driver.execute_script("window.open('');")
    moveToTab(1)
    driver.get('https://twitter.com/login')
    # driver.implicitly_wait(2)
    time.sleep(5)
    try:
        # 1: Username
        print('Username')
        driver.find_element_by_name(
            "session[username_or_email]").send_keys(twitterUser)
        # driver.implicitly_wait(2)
        # 2: Password
        print('Password')
        driver.find_element_by_name("session[password]").send_keys(twitterPwd)
        # 3: Submit button
        driver.find_element_by_xpath(
            "//div[@role='button']").click()
        time.sleep(randint(5, 10))
    except:
        """ Twitter not loaded or already logged in!"""
    closeTabs(1)


# Login to Followfast
def loginFollowfast():
    global driver
    # 1: Username
    driver.find_element_by_name(
        'username').send_keys(username)
    # 2: Password
    driver.find_element_by_name('pass').send_keys(password)
    # Some time to type the captcha
    time.sleep(5)
    # 3: Submit button
    driver.find_element_by_name('login').click()


# Global login
def login(driver):
    # MUST: Login to the main website
    loginFollowfast()
    # MUST: Login to twitter
    loginTwitter()


# Get points from Fb subscribtions
def doFbSubs():
    global driver
    driver.find_element_by_css_selector("a[href*='fbsubs.php'] ").click()
    # Switch to Fb Subs page

    foundButton = True
    while foundButton:
        try:
            followBtn = driver.find_element_by_xpath(
                "//input[@value='Follow']")
            followBtn.click()
            print("Clicked")
            time.sleep(randint(2, 4))
            closeTabs(1)
            time.sleep(randint(1, 3))
        except:
            print("No Follow button found")
            foundButton = False
    time.sleep(randint(10, 20))


def doInstaLikes():
    global driver
    driver.find_element_by_css_selector("a[href*='instb.php'] ").click()
    foundButton = True
    while foundButton:
        try:
            element = driver.find_element_by_css_selector(
                "div.likebox0")
            attributeValue = element.get_attribute("style")
            if "img/xlike-50" in attributeValue:
                driver.find_element_by_xpath("//input[@value='Like']").click()
                time.sleep(randint(5, 10))
                closeTabs(1)
                time.sleep(randint(5, 15))
            else:
                foundButton = False
        except:
            print("No Insta button found")
            foundButton = False
    time.sleep(randint(10, 20))


def doTwitterTweet():
    global driver
    driver.find_element_by_css_selector("a[href*='tweet.php'] ").click()
    time.sleep(5)
    foundButton = True
    while foundButton:
        try:
            element = driver.find_element_by_css_selector(
                "div.likebox0")
            attributeValue = element.get_attribute("style")
            # This value may change from time to time so you should update
            if "50.jpg" in attributeValue:
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                driver.find_element_by_xpath("//input[@value='Tweet']").click()
                time.sleep(1)
                moveToTab(0)
                time.sleep(2)
                driver.find_element_by_xpath("//input[@value='Tweet']").click()
                # print("We switch to the last opened tab")
                moveToTab(-1)
                # print("set_page_load_timeout")
                driver.set_page_load_timeout(0.001)
                time.sleep(0.1)
                # print("Kill last click")
                try:
                    webdriver.ActionChains(driver).send_keys(
                        Keys.ESCAPE).perform()
                except:
                    """Do nothing"""
                time.sleep(1)
                # print("We switch to the tweet page")
                moveToTab(1)
                time.sleep(5)
                # print("We switch to main page")
                moveToTab(0)
                time.sleep(1)
                # print("We close the tweet page")
                closeTabs(1)
                time.sleep(1)
                # print("We switch to main page")
                moveToTab(0)
                time.sleep(1)
                closeTabs(1)
                break
            else:
                foundButton = False
        except:
            print("No Tweet button found")
            foundButton = False
    print("We sleep randint(10, 20)")
    time.sleep(randint(10, 20))


def doTwitterLikes():
    global driver
    driver.find_element_by_css_selector("a[href*='twlike.php'] ").click()
    time.sleep(randint(10, 20))


def doTwitterRetweet():
    global driver
    driver.find_element_by_css_selector("a[href*='retweet.php'] ").click()
    time.sleep(randint(10, 20))


def doTasks():
    # doFbSubs()
    # doInstaLikes()
    doTwitterTweet()
    # doTwitterLikes()
    # doTwitterRetweet()
    time.sleep(randint(720, 1020))


if __name__ == "__main__":
    try:
        driver = loadDriver()
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        login(driver)
        while True:
            doTasks()
            # Sleep for a while to avoid bot behaviour detection
            if dt.time() > datetime.time(23):
                print("Time to sleep: 16.2 hours")
                time.sleep(60*60*9.2)
                print("We continue")
            elif dt.time() >= datetime.time(12) and dt.time() < datetime.time(13):
                print("Time to sleep: 1.3 hours")
                time.sleep(60*60*1.3)
                print("We continue")

    except:
        print("Re-try")
        driver.quit()

    # driver = loadDriver()
    # login(driver)
    # while True:
    #     doTasks()
    #     # Sleep for a while to avoid bot behaviour detection
    #     if dt.time() > datetime.time(23):
    #         print("Time to sleep: 16.2 hours")
    #         time.sleep(60*60*9.2)
    #         print("We continue")
    #     elif dt.time() >= datetime.time(12) and dt.time() < datetime.time(13):
    #         print("Time to sleep: 1.3 hours")
    #         time.sleep(60*60*1.3)
    #         print("We continue")
