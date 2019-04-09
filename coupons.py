from __future__ import print_function
from builtins import str
from builtins import input
from builtins import range
import getpass
import threading
import time
import splinter as sp
from selenium.webdriver.common.keys import Keys

MAX_WALGREENS_COUPONS = 200
CVS_PHARMACY = "CVS"
WALGREENS_PHARMACY = "Walgreens"

# Inputs
YES = 'y'
RUN_WALGREENS = 'w'
RUN_CVS = 'c'
RUN_BOTH = 'b'


class GetCoupon(threading.Thread):
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
        self.browser.quit()


def find_cvs_coupons(browser, skip_coupons):
    found_coupons = []

    found_coupons += browser.find_by_css(
        'button[ng-click="dollarOffCtrl.sentToCard($event)"]')

    found_coupons += browser.find_by_css(
        'button[ng-click="percentOffCtrl.sentToCard($event)"]')

    found_coupons += browser.find_by_css(
        'button[ng-click="manufacturerCtrl.sentToCard($event)"]')

    found_coupons += browser.find_by_css(
        'button[class="coupon__action--send2card send_to_card_coupon coupon_tile_link coupon_link_width"')

    found_coupons += filter(filter_cvs_non_coupon, browser.find_by_css(
        'p[class="mfc-prevent-backclick coupon_tile_link_colors"'))

    found_coupons = list(set(found_coupons))

    final_coupons = [
        coupon for coupon in found_coupons if coupon not in skip_coupons]

    return final_coupons


def filter_cvs_non_coupon(button):
    return button.text.lower() == "send to card"


def find_walgreens_coupons(browser):
    return browser.find_by_css('button[title="Clip coupon"]')


# Counts Walgreens Coupons that have been clipped
def count_walgreens_coupons(browser):
    time.sleep(5)
    return browser.find_by_css('a[title="View Coupons clipped"] > strong').text


def get_credentials(pharmacy, credentials):
    print("")
    print("Before saving you money at " + pharmacy + ", you have to log in.")
    print("Please input your login credentials for " +
          pharmacy + ". When you have done so, press enter.")
    email = input("What's your " + pharmacy + " account id? ")
    pwd = getpass.getpass()
    credentials[pharmacy] = {"email": email, "pwd": pwd}
    print("Thanks! Continuing...")
    print("")


def log_in(pharmacy, credentials, browser):
    email = credentials[pharmacy]["email"]
    pwd = credentials[pharmacy]["pwd"]

    if pharmacy is CVS_PHARMACY:
        browser.find_by_id('email').fill(email)
        time.sleep(2)
        active_web_element = browser.driver.switch_to.active_element
        active_web_element.send_keys(Keys.ENTER)
        time.sleep(2)
        browser.find_by_id('password').fill(pwd)
        time.sleep(2)
        active_web_element = browser.driver.switch_to.active_element
        active_web_element.send_keys(Keys.ENTER)
    elif pharmacy is WALGREENS_PHARMACY:
        terms = browser.find_by_css('a[class="action__close-modal"]')
        if terms:
            terms[0].click()
            time.sleep(1)
        browser.find_by_css('input[name="userNameOrPhone"]').fill(email)
        time.sleep(2)
        active_web_element = browser.driver.switch_to.active_element
        active_web_element.send_keys(Keys.ENTER)
        time.sleep(2)
        browser.find_by_css('input[name="password"]').fill(pwd)
        time.sleep(2)
        active_web_element = browser.driver.switch_to.active_element
        active_web_element.send_keys(Keys.ENTER)

    time.sleep(6)


def beat_captcha():
    print("Pass the CAPTCHA on the page so that the script can continue.")
    while True:
        choice = input("Have you passed the CAPTCHA? (y/n): ")
        if choice is YES:
            return

        print("Try again. If you weren't able to beat the CAPTCHA, close the script with control+C and restart")


def choose_pharmacy():
    print("For which pharmacy would you like to save coupons?")
    while True:
        choice = input("If Walgreens, press 'w'. For CVS, press 'c'. For " +
                       "both, press 'b'. After making your choice, press " +
                       "Enter. Thanks!\n")
        if choice is RUN_WALGREENS:
            return [(walgreens, WALGREENS_PHARMACY)]
        if choice is RUN_CVS:
            return [(cvs, CVS_PHARMACY)]
        if choice is RUN_BOTH:
            return [(walgreens, WALGREENS_PHARMACY), (cvs, CVS_PHARMACY)]

        print("I'm sorry, I didn't understand that. Try again.")


def cvs(credentials, browser):
    print("Preparing to save some CVS coupons!")
    browser.visit("https://www.cvs.com/account/login/")
    beat_captcha()
    log_in(CVS_PHARMACY, credentials, browser)
    browser.visit('https://www.cvs.com/extracare/home')
    time.sleep(5)

    # Try to scroll to bottom
    print("CVS: Scrolling to bottom of page")
    scroll_number = 30
    for scroll in range(scroll_number):
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        if (scroll % 5 == 0 and scroll != scroll_number):
            remaining_scroll = scroll_number - scroll
            print("CVS: Scrolling " + str(remaining_scroll) + " more times")
        time.sleep(3)

    print("CVS: Finished scrolling")
    skip_coupons = []
    coupons = find_cvs_coupons(browser, skip_coupons)

    error_count = 0
    while coupons:
        error_count += 1
        if error_count > 5:
            break
        browser.execute_script("window.scrollTo(0, 0);")
        for coupon in coupons:
            try:
                time.sleep(1)
                coupon.click()
            except:
                break

            # try:
            #     # TODO: Test this!
            #     # <p class="error_s2c">We're sorry. We're not able to send this coupon to your card. Please try again later or call us at 1-800-SHOP CVS for help.</p>
            #     if browser.find_by_text("We're sorry. We're not able to " +
            #                             "send this coupon to your card. " +
            #                             "Please try again later or call " +
            #                             "us at 1-800-SHOP CVS for help."):
            #         skip_coupons.append(coupon)
            #         print("CVS: There was an error saving a coupon.")
            # except:
            #     # TODO: Test this!
            #     # <p class="error_s2c">We're sorry. We're not able to send this coupon to your card. Please try again later or call us at 1-800-SHOP CVS for help.</p>
            #     if browser.find_by_text("We're sorry. We're not able to " +
            #                             "send this coupon to your card. " +
            #                             "Please try again later or call " +
            #                             "us at 1-800-SHOP CVS for help."):
            #         skip_coupons.append(coupon)
            #         print("CVS: There was an error saving a coupon.")
            #     coupons = find_cvs_coupons(browser, skip_coupons)
            #     try:
            #         if coupons:
            #             coupons[0].click()
            #     except:
            #         pass
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        coupons = find_cvs_coupons(browser, skip_coupons)

    print("CVS: " + str(len(skip_coupons)) + " were skipped.")
    return CVS_PHARMACY


def walgreens(credentials, browser):
    print("Preparing to save some Walgreens coupons!")
    browser.visit('https://www.walgreens.com/login.jsp')
    log_in(WALGREENS_PHARMACY, credentials, browser)
    browser.visit('https://www.walgreens.com/offers/offers.jsp')
    time.sleep(5)

    close_overlay = browser.find_by_css('button[id="closeWelcomeBOverlay"]')
    if close_overlay:
        close_overlay[0].click()
        time.sleep(1)

    coupons_saved = count_walgreens_coupons(browser)

    print("Walgreens: Currently have: " + coupons_saved + " saved!")
    print("Walgreens: The theoretical maximun number of coupons allowed is " +
          str(MAX_WALGREENS_COUPONS))
    remaining = MAX_WALGREENS_COUPONS - int(coupons_saved)

    if remaining > 0:
        coupons = find_walgreens_coupons(browser)
        while coupons:
            browser.execute_script("window.scrollTo(0, 0);")
            for coupon in coupons:
                max_reached = browser.find_by_css('h3[id="confMessageCoupon"]')
                if remaining <= 0 or max_reached:
                    return WALGREENS_PHARMACY
                try:
                    coupon.click()
                    remaining -= 1
                except:
                    time.sleep(2)
                    coupons = find_walgreens_coupons(browser)
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            coupons = find_walgreens_coupons(browser)

    return WALGREENS_PHARMACY


def end(pharmacy):
    print(pharmacy + ": All possible " + pharmacy +
          " coupons sent to card! Go save some money :)")


def main():
    pharmacies = choose_pharmacy()
    credentials = {}
    threads = []
    for pharmacy in pharmacies:
        get_credentials(pharmacy[1], credentials)

    for pharmacy in pharmacies:
        threads.append(GetCoupon(pharmacy, credentials, sp.Browser('chrome')))

    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
