import splinter as sp
from threading import Timer
import time

def findCoupons():
	return browser.find_by_css('img[class="sendCardIcon"]')

def logIn():
	print "For this script to work, you have to log in."
	print "Please log in to CVS. When you have done so, please follow the instructions here."
	raw_input("Press Enter to continue...")
	print "Thanks! Continuing..."

browser = sp.Browser('chrome')
browser.visit('https://www.cvs.com/')
logIn()
browser.visit('https://www.cvs.com/extracare/home')
time.sleep(5)

# Try to scroll to bottom
for x in xrange(1,25):
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(3)

coupons = findCoupons()

while coupons:
	for coupon in coupons:
		try:
			coupon.click()
		except:
			time.sleep(2)
			coupons = findCoupons()
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(5)
	coupons = findCoupons()

print "All coupons sent to card! Go save some money :)"
