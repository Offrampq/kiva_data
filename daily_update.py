## step 3 

#### import
from datetime import datetime
import dateutil.parser
from time import strptime
from lxml import html
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen, Request, HTTPError, URLError
import sys  
import urlparse
import urllib2
import json
import mysql.connector


# today's date 
i = datetime.utcnow()
year = i.year
month = i.month
day = i.day

### make soup
def make_soup(url):
	try:
		urllib2.urlopen(url)
	except HTTPError, e:
		print e.code
	except URLError, e:
		print e.reason
	else:
		html = urlopen(url).read()
		soup = BeautifulSoup(html, "lxml")
		return soup

# get all ids
def get_lenders_list():
	conn = mysql.connector.connect(user = 'Qinghui', password = None, host = '127.0.0.1', database = 'test')
	cur = conn.cursor()
	cur.execute("select bi.id from basic_info1 as bi where bi.id not in (select du.id from daily_update as du where du.togo = 'funded' group by du.id)")
	ol = cur.fetchall()
	conn.commit()
	conn.close()
	id_list = []
	for o in ol:
		id_list.append(o[0])
	return id_list


# get fund update
def get_update(u, i):
	print u
	url = 'http://www.kiva.org/lend/' + str(u)
	soup = make_soup(url)
	t1= soup.findAll(attrs = {"class": "amountLeft"})
	if len(t1) != 0:
		togo = t1[0].string.split()[1]
	else:
		togo = 'funded'
	return {'togo': togo, 'datetime': str(i), 'id':u}


# insert into daily_update_table
def insert_daily_update(all_ids,i):
	conn = mysql.connector.connect(user = 'Qinghui', password = None, host = '127.0.0.1', database = 'test')
	cur = conn.cursor()
	for u in all_ids:
		p = get_update(u,i)
		cur.execute("insert into daily_update (id, datetime, togo) values(%(id)s, %(datetime)s, %(togo)s)", p)
		conn.commit()
	conn.close()
	print 'daily_update done'



######################################################
# main
######################################################
all_ids = get_lenders_list()
insert_daily_update(all_ids,i)











