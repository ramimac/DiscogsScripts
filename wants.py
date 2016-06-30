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

response = br.open('https://www.discogs.com/sell/mywants?ev=wsim#more%%3Dseller')
res = response.get_data()
soup = BeautifulSoup(res, "lxml")
for seller in soup.find_all(class_='filter_seller')[0].contents[1].find_all('a')[:-1]:
	number = seller.find(class_='facet_count').contents[0]
	text = seller['href']
	name = re.search(u'/seller/(.+)/mywants\?ev=wsim', text).group(1)
	print name.upper() + " ----- " + number
	response = br.open('https://www.discogs.com/seller/' + name + '/mywants?ev=wsim')
	resp = response.get_data()
	soup = BeautifulSoup(resp, "lxml")
	links = soup.find_all(class_="item_release_link")
	records = soup.find_all(class_="item_description_title")
	prices = soup.find_all(class_="price")
	for link, record, price in itertools.izip(links, records, prices[::2]):
		recid = re.search(u'/.+/.+/(.+)', link['href']).group(1)
		response = br.open('https://www.discogs.com/sell/history/'+recid)
		datum = response.get_data()
		soup = BeautifulSoup(datum, "lxml")
		historicprices = str(soup.find_all(class_='clearfix')[0])
		lowest = re.search(u'\$(.*)\n\s*<small>Lowest', historicprices).group(1)
		print record.contents[0] + " ..... " + price.contents[0] + " ~~~~~ " + lowest



