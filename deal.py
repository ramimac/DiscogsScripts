#!/usr/bin/env python

import mechanize
import wantsconfig as wc
from bs4 import BeautifulSoup
import re
import itertools

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) Chrome/50.0.2661.75 Safari/537.36')]
br.open('https://www.discogs.com/login')
br.select_form(nr=1)
br['username'] = wc.username 
br['password'] = wc.password
response = br.submit()

url = 'https://www.discogs.com/sell/mywants?sort=listed%%2Cdesc&limit=250&ev=wsim&page='
page = 1

while True:
	response = br.open(url+str(page))
	res = response.get_data()
	soup = BeautifulSoup(res, "lxml")
	print page

	## out of pages
	if len(soup.find_all(text = 'No items for sale found'))>0:
		break
	else:
		## pull price, pull lowest ever price, compare - if lower 
		## lowest ever, print name, seller, cost
		page += 1

