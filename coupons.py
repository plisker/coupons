from __future__ import print_function
from builtins import str
from builtins import input
from builtins import range
import splinter as sp
import time
from selenium.webdriver.common.keys import Keys
import getpass

MAX_WALGREENS_COUPONS = 200

def findCVSCoupons(browser):
	return browser.find_by_css('img[class="sendCardIcon"]')

def findWalgreensCoupons(browser):
	return browser.find_by_css('button[title="Clip coupon"]')

# Counts Walgreens Coupons that have been clipped
def countWalgreensCoupons(browser):
	time.sleep(5)
	return browser.find_by_css('a[title="View Coupons clipped"] > span').text

def logIn(pharmacy, browser):
	print("")
	print("Before saving you money, you have to log in.")
	print("Please input your login credentials for "+ pharmacy +". When you have done so, press enter.")
	email = input("What's your "+ pharmacy +" account id? ")
	pswd = getpass.getpass()

	if pharmacy is "CVS":
		browser.find_by_css('a[title="opens in a new window"]').click()
		time.sleep(1)
		browser.find_by_id('loginPopup').fill(email)
		browser.find_by_id('passwordPopup').fill(pswd)
		active_web_element = browser.driver.switch_to_active_element()
		active_web_element.send_keys(Keys.ENTER)
	elif pharmacy is "Walgreens":
		terms = browser.find_by_css('a[class="action__close-modal"]')
		if terms:
			terms[0].click()
			time.sleep(1)
		browser.find_by_css('input[name="userNameOrPhone"]').fill(email)
		active_web_element = browser.driver.switch_to_active_element()
		active_web_element.send_keys(Keys.ENTER)
		time.sleep(1)
		browser.find_by_css('input[name="password"]').fill(pswd)
		active_web_element = browser.driver.switch_to_active_element()
		active_web_element.send_keys(Keys.ENTER)

	print("Thanks! Continuing...")
	time.sleep(8)

def choosePharmacy():
	print("For which pharmacy would you like to save coupons?")
	while True:
		choice = input("If Walgreens, press 'w'. For CVS, press 'c'. For both, press 'b'. After making your choice, press Enter. Thanks!\n")
		if choice is 'w':
			return [walgreens]
		elif choice is 'c':
			return [cvs]
		elif choice is 'b':
			return [walgreens, cvs]
		else:
			print("I'm sorry, I didn't understand that. Try again.")

def cvs(browser):
	print("Preparing to save some CVS coupons!")
	browser.visit('https://www.cvs.com/')
	logIn("CVS", browser)
	browser.visit('https://www.cvs.com/extracare/home')
	time.sleep(5)

	# Try to scroll to bottom
	for x in range(25):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)

	coupons = findCVSCoupons(browser)

	while coupons:
		browser.execute_script("window.scrollTo(0, 0);")
		for coupon in coupons:
			try:
				time.sleep(2)
				coupon.click()
			except:
				coupons[0].click()
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(5)
		coupons = findCVSCoupons(browser)

	return "CVS"

def walgreens(browser):
	print("Preparing to save some Walgreens coupons!")
	browser.visit('https://www.walgreens.com/login.jsp')
	logIn("Walgreens", browser)
	browser.visit('https://www.walgreens.com/offers/offers.jsp')
	time.sleep(5)

	close_overlay = browser.find_by_css('button[id="closeWelcomeBOverlay"]')
	if close_overlay:
		close_overlay[0].click()
		time.sleep(1)

	couponsSaved = countWalgreensCoupons(browser)

	print("Currently have: "+ couponsSaved +" saved!")
	print("The theoretical maximun number of coupons allowed is " + str(MAX_WALGREENS_COUPONS))
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
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(5)
			coupons = findWalgreensCoupons(browser)

	return "Walgreens"

def end(pharmacy):
	print("All possible " + pharmacy + " coupons sent to card! Go save some money :)")

def main():
	pharmacies = choosePharmacy()
	browser = sp.Browser('chrome')
	for pharmacy in pharmacies:
		name = pharmacy(browser)
		end(name)
	browser.quit()

if __name__ == "__main__":
    main()
