import splinter as sp
import time

MAX_WALGREENS_COUPONS = 200

def findCVSCoupons(browser):
	return browser.find_by_css('img[class="sendCardIcon"]')

def findWalgreensCoupons(browser):
	return browser.find_by_css('button[title="Clip coupon"]')

def countWalgreensCoupons(browser):
	return browser.find_by_css('a[title="Coupons clipped - to show clipped coupons"] > span').text

def logIn(pharmacy):
	print "For this script to work, you have to log in."
	print "Please log in to "+ pharmacy +". When you have done so, please follow the instructions here."
	raw_input("Press Enter to continue...")
	print "Thanks! Continuing..."

def choosePharmacy():
	print "For which pharmacy would you like to save coupons?"
	pharmacies = []
	while not pharmacies:
		input = raw_input("If Walgreens, press 'w'. For CVS, press 'c'. For both, press 'b'. After making your choice, press Enter. Thanks!\n")
		if input is 'w':
			pharmacies.append(walgreens)
		elif input is 'c':
			pharmacies.append(cvs)
		elif input is 'b':
			pharmacies.append(walgreens)
			pharmacies.append(cvs)
		else:
			print "I'm sorry, I didn't understand that. Try again."

	return pharmacies

def cvs():
	browser = sp.Browser('chrome')
	browser.visit('https://www.cvs.com/')
	logIn("CVS")
	browser.visit('https://www.cvs.com/extracare/home')
	time.sleep(5)

	# Try to scroll to bottom
	for x in xrange(1,25):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)

	coupons = findCVSCoupons(browser)

	while coupons:
		browser.execute_script("window.scrollTo(0, 0);")
		for coupon in coupons:
			try:
				coupon.click()
			except:
				time.sleep(2)
				coupons = findCVSCoupons(browser)
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(5)
		coupons = findCVSCoupons(browser)

	return "CVS"

def walgreens():
	browser = sp.Browser('chrome')
	browser.visit('https://www.walgreens.com/')
	logIn("Walgreens")
	browser.visit('https://www.walgreens.com/offers/offers.jsp')
	time.sleep(5)

	couponsSaved = countWalgreensCoupons(browser)

	print "Currently have: "+ couponsSaved +" saved!"
	print "The theoretical maximun number of coupons allowed is " + str(MAX_WALGREENS_COUPONS)
	remaining = MAX_WALGREENS_COUPONS - int(couponsSaved)

	if remaining > 0:
		coupons = findWalgreensCoupons(browser)
		while coupons:
			browser.execute_script("window.scrollTo(0, 0);")
			counter = 0
			for coupon in coupons:
				if remaining <= 0:
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
	print "All possible " + pharmacy + " coupons sent to card! Go save some money :)"

def main():
	pharmacies = choosePharmacy()
	for pharmacy in pharmacies:
		name = pharmacy()
		end(name)

if __name__ == "__main__":
    main()
