from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# Display exception
import traceback
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
    # Full screen display
    options.add_argument("start-maximized")
    # start chrome without showing the browser
    # options.add_argument('headless')
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # END start chrome without showing the browser
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
            time.sleep(randint(3, 5))
        except:
            print("No Follow button found")
            foundButton = False
    time.sleep(randint(5, 10))


def doInstaLikes():
    global driver
    driver.find_element_by_css_selector("a[href*='instb.php'] ").click()
    foundButton = True
    index = 0
    while foundButton and index < 20:
        try:
            element = driver.find_element_by_css_selector(
                "div.likebox0")
            attributeValue = element.get_attribute("style")
            if "img/xlike-50" in attributeValue:
                driver.find_element_by_xpath("//input[@value='Like']").click()
                time.sleep(randint(5, 10))
                closeTabs(1)
                time.sleep(randint(15, 25))
                index += 1
            else:
                foundButton = False
        except:
            print("No Insta button found")
            foundButton = False
    time.sleep(randint(10, 20))


def twitterWorkFlow(TweetOrLoveOrRetwt):
    global driver
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
    # Do Tweets
    time.sleep(5)
    doTwitterTweet()
    time.sleep(3)
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


def doTwitter():
    global driver
    driver.find_element_by_css_selector("a[href*='tweet.php'] ").click()
    time.sleep(5)
    foundButton = True
    index = 0
    while foundButton and index < 20:
        try:
            element = driver.find_element_by_css_selector(
                "div.likebox0")
            attributeValue = element.get_attribute("style")
            # This value may change from time to time so you should update
            if "50.jpg" in attributeValue:
                twitterWorkFlow("Tweet")
                index += 1
                time.sleep(randint(5, 10))
            else:
                foundButton = False
        except:
            print("No Tweet button found")
            foundButton = False
    print("We sleep randint(10, 20)")
    time.sleep(randint(10, 20))


def doTwitterTweet():
    global driver
    driver.set_page_load_timeout(30)
    print("Set random to avoid twitter existing post warning ")
    try:
        span = driver.find_element_by_xpath(
            "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div/div/div/div/span[2]/span")
        driver.execute_script(
            "arguments[0].innerText = '"+str(randint(100, 900))+"'", span)
    except:
        """ DO NOTHING """
    time.sleep(0.5)
    print("Click Tweet button")
    try:
        driver.find_element_by_xpath(
            "//div[@role='button'][@data-testid='tweetButton'][@tabindex='0']").click()
        webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
    except Exception as e:
        print(e)


def doTwitterLikes():
    global driver
    driver.find_element_by_css_selector("a[href*='twlike.php'] ").click()
    time.sleep(randint(10, 20))


def doTwitterRetweet():
    global driver
    driver.find_element_by_css_selector("a[href*='retweet.php'] ").click()
    time.sleep(randint(10, 20))


def doTasks():
    global driver
    for i in range(3):
        driver.refresh()
        time.sleep(3.5)
        doFbSubs()
        doInstaLikes()
        doTwitter()
        # doTwitterLikes()
        # doTwitterRetweet()
    sleepingTime = randint(720, 1020)
    print("sleepingTime: "+str(sleepingTime/60))
    time.sleep(sleepingTime)


if __name__ == "__main__":
    try:
        driver = loadDriver()
        login(driver)
        while True:
            try:
                doTasks()
            except:
                """ Just ignore the exception to not lose the session"""
    except:
        print("Re-try")
        driver.quit()
