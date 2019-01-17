from __future__ import print_function
from builtins import str
from builtins import input
from builtins import range
import threading
import splinter as sp
import time
from selenium.webdriver.common.keys import Keys
import getpass

MAX_WALGREENS_COUPONS = 200


class GetCoupon (threading.Thread):
    def __init__(self, pharmacy, credentials, browser):
        threading.Thread.__init__(self)
        self.pharmacy = pharmacy
        self.credentials = credentials
        self.browser = browser
        self.pharmacy = pharmacy[0]
        self.name = pharmacy[1]

    def run(self):
        self.pharmacy(self.credentials, self.browser)
        end(self.name)
        browser.quit()


def findCVSCoupons(browser):
    return browser.find_by_css('button[class="coupon__action--send2card send_to_card_coupon coupon_tile_link coupon_link_width"]')


def findWalgreensCoupons(browser):
    return browser.find_by_css('button[title="Clip coupon"]')


# Counts Walgreens Coupons that have been clipped
def countWalgreensCoupons(browser):
    time.sleep(5)
    return browser.find_by_css('a[title="View Coupons clipped"] > strong').text


def getCredentials(pharmacy, credentials):
    print("")
    print("Before saving you money at " + pharmacy + ", you have to log in.")
    print("Please input your login credentials for " +
          pharmacy + ". When you have done so, press enter.")
    email = input("What's your " + pharmacy + " account id? ")
    pwd = getpass.getpass()
    credentials[pharmacy] = {"email": email, "pwd": pwd}
    print("Thanks! Continuing...")
    print("")


def logIn(pharmacy, credentials, browser):

    email = credentials[pharmacy]["email"]
    pwd = credentials[pharmacy]["pwd"]

    if pharmacy is "CVS":
        browser.find_by_id('signInBtn').click()
        time.sleep(1)
        browser.find_by_id('clubLoginEmail').fill(email)
        browser.find_by_id('clubLoginPwd').fill(pwd)
        active_web_element = browser.driver.switch_to.active_element
        active_web_element.send_keys(Keys.ENTER)
    elif pharmacy is "Walgreens":
        terms = browser.find_by_css('a[class="action__close-modal"]')
        if terms:
            terms[0].click()
            time.sleep(1)
        browser.find_by_css('input[name="userNameOrPhone"]').fill(email)
        active_web_element = browser.driver.switch_to.active_element
        active_web_element.send_keys(Keys.ENTER)
        time.sleep(1)
        browser.find_by_css('input[name="password"]').fill(pwd)
        active_web_element = browser.driver.switch_to.active_element
        active_web_element.send_keys(Keys.ENTER)

    time.sleep(8)


def choosePharmacy():
    print("For which pharmacy would you like to save coupons?")
    while True:
        choice = input("If Walgreens, press 'w'. For CVS, press 'c'. For " +
                       "both, press 'b'. After making your choice, press " +
                       "Enter. Thanks!\n")
        if choice is 'w':
            return [(walgreens, "Walgreens")]
        elif choice is 'c':
            return [(cvs, "CVS")]
        elif choice is 'b':
            return [(walgreens, "Walgreens"), (cvs, "CVS")]
        else:
            print("I'm sorry, I didn't understand that. Try again.")


def cvs(credentials, browser):
    print("Preparing to save some CVS coupons!")
    browser.visit('https://www.cvs.com/')
    logIn("CVS", credentials, browser)
    browser.visit('https://www.cvs.com/extracare/home')
    time.sleep(5)

    # Try to scroll to bottom
    for x in range(25):
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    coupons = findCVSCoupons(browser)

    while coupons:
        browser.execute_script("window.scrollTo(0, 0);")
        for coupon in coupons:
            try:
                time.sleep(1)
                coupon.click()
            except:
                coupons = findCVSCoupons(browser)
                try:
                    if coupons:
                        coupons[0].click()
                except:
                    pass
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        coupons = findCVSCoupons(browser)

    return "CVS"


def walgreens(credentials, browser):
    print("Preparing to save some Walgreens coupons!")
    browser.visit('https://www.walgreens.com/login.jsp')
    logIn("Walgreens", credentials, browser)
    browser.visit('https://www.walgreens.com/offers/offers.jsp')
    time.sleep(5)

    close_overlay = browser.find_by_css('button[id="closeWelcomeBOverlay"]')
    if close_overlay:
        close_overlay[0].click()
        time.sleep(1)

    couponsSaved = countWalgreensCoupons(browser)

    print("Walgreens: Currently have: " + couponsSaved + " saved!")
    print("Walgreens: The theoretical maximun number of coupons allowed is " +
          str(MAX_WALGREENS_COUPONS))
    remaining = MAX_WALGREENS_COUPONS - int(couponsSaved)

    if remaining > 0:
        coupons = findWalgreensCoupons(browser)
        while coupons:
            browser.execute_script("window.scrollTo(0, 0);")
            for coupon in coupons:
                max_reached = browser.find_by_css('h3[id="confMessageCoupon"]')
                if remaining <= 0 or max_reached:
                    return "Walgreens"
                try:
                    coupon.click()
                    remaining -= 1
                except:
                    time.sleep(2)
                    coupons = findWalgreensCoupons(browser)
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            coupons = findWalgreensCoupons(browser)

    return "Walgreens"


def end(pharmacy):
    print(pharmacy + ": All possible " + pharmacy +
          " coupons sent to card! Go save some money :)")


def main():
    pharmacies = choosePharmacy()
    credentials = {}
    threads = []
    for pharmacy in pharmacies:
        getCredentials(pharmacy[1], credentials)

    for pharmacy in pharmacies:
        threads.append(GetCoupon(pharmacy, credentials, sp.Browser('chrome')))

    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
