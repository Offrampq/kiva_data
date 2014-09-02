## step 1

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


# get the list
def get_lenders_list():
	url = 'http://api.kivaws.org/v1/loans/newest.json'
	data = json.load(urllib2.urlopen(url))
	lender_list = {}
	for a in range(0,20):
		ii = data['loans'][a]['id']
		basic_1 = {}
		for b in data['loans'][a]:
			basic_1[b] = data['loans'][a][b]
		lender_list[ii] = basic_1
	return lender_list


### check if the lender is from today
def check_latest(t, i):
	nt = datetime.date(dateutil.parser.parse(t))
	ni = datetime.date(i)
	if nt == ni:
		return True
	else:
		return False


# obtain today_list
def get_old_id_list():
	conn = mysql.connector.connect(user = 'Qinghui', password = None, host = '127.0.0.1', database = 'test')
	cur = conn.cursor()
	cur.execute("select id from today_list group by id")
	ol = cur.fetchall()
	conn.commit()
	conn.close()
	old_list = []
	for o in ol:
		old_list.append(o[0])
	return old_list


# update today_list
def update_id_list(lender_list, old_list):
	new_list = []
	for o in old_list:
		new_list.append(o)
	for ll in lender_list:
		t = lender_list[ll]['posted_date']
		if check_latest(t,i) and (ll not in new_list):
			# print 'yes'
			new_list.append(ll)
	conn = mysql.connector.connect(user = 'Qinghui', password = None, host = '127.0.0.1', database = 'test')
	cur = conn.cursor()
	cur.execute("truncate table today_list")
	conn.commit()
	for o in new_list:
		lend_id = {'id': o}
		cur.execute("insert into today_list (id) values(%(id)s)", lend_id)	
	conn.commit()
	conn.close()
	print 'update today_list'
	return new_list


# check what's already in basic_info1
def already_exist():
	conn = mysql.connector.connect(user = 'Qinghui', password = None, host = '127.0.0.1', database = 'test')
	cur = conn.cursor()
	cur.execute("select id from basic_info1 group by id")
	res = cur.fetchall()
	ae = []
	for a in res:
		ae.append(a[0])
	return ae


# get basic info 1
def insert_basic_info1(lender_list, ae):
	conn = mysql.connector.connect(user = 'Qinghui', password = None, host = '127.0.0.1', database = 'test')
	cur = conn.cursor()
	for ll in lender_list:
		if ll not in ae:
			basic = lender_list[ll]
			print ll
			add_info = {}
			add_info["funded_amount"] = basic["funded_amount"] 
			add_info["purpose"] = basic["use"]
			add_info["posted_date"] = basic["posted_date"]
			# add_info["basket_amount"] = basic["basket_amount"] 
			add_info["sector"] = basic["sector"]
			add_info["borrower_count"] = basic["borrower_count"] 
			add_info["bonus_credit_eligibility"] = basic["bonus_credit_eligibility"] 
			add_info["loan_amount"] = basic["loan_amount"] 
			add_info["country"] = basic["location"]["country"] 
			add_info["longlat"] = basic["location"]["geo"]["pairs"]
			add_info["planned_expiration_date"] = basic["planned_expiration_date"]
			add_info["activity"] = basic["activity"]
			add_info["partner_id"] = basic["partner_id"] 
			add_info["id"] = basic["id"] 
			# print add_info
			cur.execute("insert into basic_info1 (funded_amount,purpose,posted_date,sector,borrower_count,bonus_credit_eligibility,loan_amount,country,longlat,planned_expiration_date,activity,partner_id,id) values(%(funded_amount)s,%(purpose)s,%(posted_date)s,%(sector)s,%(borrower_count)s,%(bonus_credit_eligibility)s,%(loan_amount)s,%(country)s,%(longlat)s,%(planned_expiration_date)s,%(activity)s,%(partner_id)s,%(id)s)", add_info)
			conn.commit()
			print 'insert 1'
	conn.close()
	print 'done inserting basic_info1'



######################################################
# main
######################################################
lender_list = get_lenders_list()
old_list = get_old_id_list()
new_list = update_id_list(lender_list, old_list)
ae = already_exist()
insert_basic_info1(lender_list, ae)





