#!/usr/bin/python

import argparse
import SeCupid.SeCupid as SeCupid

def scrape(usr, psw):
	# cupid = SeCupid.SeCupid(usr, psw, headless=True)
	cupid = SeCupid.SeCupid(usr, psw, headless=False)
	cupid.login()
	while cupid.scrape:
		cupid.getAllUsers()
	for user in cupid.db.getOkcupidUsers():
		try:
			cupid.saveProfile(user.username)
		except Exception as e:
			cupid.takeScreenShot(user.username)
	cupid.driver.quit()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Selenium OkCupid')
	parser.add_argument('-u', 
						type=str,
						required=True,
						help='okcupid username')
	parser.add_argument('-p', 
						type=str,
					 	required=True,
						help='okcupid password')
	args = parser.parse_args()
	scrape(args.u, args.p)
