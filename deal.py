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

url = 'https://www.discogs.com/sell/mywants?currency=USD&ev=wsim&page='
page = 1

while True:
	response = br.open(url+str(page))
	res = response.get_data()
	soup = BeautifulSoup(res, "lxml")
	soup_str = str(soup)
	## out of pages
	if len(soup.find_all(text = 'No items for sale found'))>0:
		break
	else:
		## pull price, pull lowest ever price, compare - if lower 
		## lowest ever, print name, seller, cost
		# get links, titles, and prices
		links = soup.find_all(class_="item_release_link")
		records = soup.find_all(class_="item_description_title")
		prices = soup.find_all(class_="price")[::2]
		sellers = re.findall(u'/seller/(.+)/profile', soup_str)
		for link, record, price, seller in itertools.izip(links, records, prices, sellers):
			#get lowest ever price, store in lowest
			recid = re.search(u'/.+/.+/(.+)', link['href']).group(1)
			response = br.open('https://www.discogs.com/sell/history/'+recid)
			datum = response.get_data()
			soup = BeautifulSoup(datum, "lxml")
			if len(soup.find_all(class_='clearfix')) == 0:
				historicprices = int(0)
				lowest = int(0)
			else:
				historicprices = str(soup.find_all(class_='clearfix')[0])
				lowest = re.search(u'\$(.*)\n\s*<small>Lowest', historicprices).group(1)
			if float(price.contents[0][1:]) < float(lowest):
			## IMPORTANT PRINT INFO
				print seller+' is selling '+record.contents[0]+' for '+price.contents[0]
				print '\t'+'The previous lowest price was: $'+lowest
		page += 1


