## step 2

#### import
from datetime import datetime
import dateutil.parser
from time import strptime
from lxml import html
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen, Request, HTTPError, URLError
import urllib
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


### download main image
def download_image(image_url):
	# download images
	response = requests.get(image_url)  
	parsed_body = html.fromstring(response.text)
	# Grab links to all images
	images = parsed_body.xpath('//img/@src')  
	if not images:  
	    sys.exit("Found No Images")
	# Convert any relative urls to absolute urls
	images = [urlparse.urljoin(response.url, url) for url in images]  
	#print 'Found %s images' % len(images)
	# Only download first 10
	r = requests.get(images[1])
	f = open('Dropbox/kiva/images/%s' % image_url.split('/')[-1] + '.jpg', 'w')
	f.write(r.content)
	f.close()


# download all pictures
def download_all_images(today_list_ids):
	for u in today_list_ids:
		image_url = 'http://www.kiva.org/lend/' + str(u)
		#print image_url
		download_image(image_url)
	print 'All images of the day done'


### getting basic info
def get_basic2(u):
	url = 'http://www.kiva.org/lend/' + str(u)
	keywords_list = ["son", "daughter", "kid", "child", "enfant", "school"]
	soup = make_soup(url)
	# gender
	sc = soup.findAll("script")
	gender_m = 2
	if 'gender' in sc[6].string:
		ind = sc[6].string.index('gender')
		if sc[6].string[ind + 9] == 'm':
			gender_m = 1
		else:
			gender_m = 0
	# repayment term
	all_dd = soup.findAll("dd")
	term = all_dd[0].get_text().split()[0]
	# loan discription - children_flag. Key words "son", "daughter", "kid", "child", "enfant"
	dis = soup.findAll(attrs = {"class": "loanDescription introText"})[0].get_text()
	child_flag = 0
	for w in keywords_list:
		if w in dis:
			child_flag = 1
	# field partner due diligence type
	due_dil_type = all_dd[6].get_text()
	# field partner rating
	t1= soup.findAll(attrs = {"class": "partnerRating active halves"})
	if len(t1) != 0:
		t2 = t1[0].attrs.get('title')
		p_rating = t2.split()[3]
	else: 
		p_rating = 99
	# time on kiva
	t1 = all_dd[8].get_text()
	p_time_on_kiva = t1.split()[0]
	# kiva borrowers
	t1 = all_dd[9].get_text()
	p_borrowers = t1.strip()
	# total loans
	t1 = all_dd[10].get_text()
	p_total_loans = t1.strip()
	# interest charged (y/n)
	t1 = all_dd[11].get_text()
	interest_charged = t1.strip()
	# Avg cost to borrower
	t1 = all_dd[12].get_text()
	avg_cost_borrower = t1.strip()
	# profitablity
	t1 = all_dd[13].get_text()
	profitablity = t1.strip()
	# avg loan size per capita income
	t1 = all_dd[14].get_text()
	loan_ppc = t1.strip()
	# deliquency rate
	t1 = all_dd[15].get_text()
	deliquency = t1.strip()
	# loans at risk rate
	t1 = all_dd[16].get_text()
	risk_rate = t1.strip()
	# default rate
	t1 = all_dd[17].get_text()
	default_rate = t1.strip()
	# currency exchange loss rate
	t1 = all_dd[18].get_text()
	loss_rate = t1.strip()
	return {"id": u, "gender_m": gender_m, "term": unicode(term),"child_flag": child_flag,"due_dil_type": unicode(due_dil_type),"p_rating": unicode(p_rating),"p_time_on_kiva": unicode(p_time_on_kiva),"p_borrowers": unicode(p_borrowers),"p_total_loans": unicode(p_total_loans),"interest_charged": unicode(interest_charged),"avg_cost_borrower": unicode(avg_cost_borrower),"profitablity": unicode(profitablity),"loan_ppc": unicode(loan_ppc),"deliquency": unicode(deliquency),"risk_rate": unicode(risk_rate),"default_rate": unicode(default_rate),"loss_rate": unicode(loss_rate)}


# check what's already in basic_info2
def already_exist():
	conn = mysql.connector.connect(user = 'Qinghui', password = None, host = '127.0.0.1', database = 'test')
	cur = conn.cursor()
	cur.execute("select id from basic_info2 group by id")
	res = cur.fetchall()
	ae = []
	for a in res:
		ae.append(a[0])
	return ae


# insert into basic_info2
def insert_basic_info2(today_list_ids, ae):
	conn = mysql.connector.connect(user = 'Qinghui', password = None, host = '127.0.0.1', database = 'test')
	cur = conn.cursor()
	for u in today_list_ids:
		if u not in ae:
			print u
			basic = get_basic2(u)
			cur.execute("insert into basic_info2 (gender_m, term, child_flag, due_dil_type, p_rating, p_time_on_kiva, p_borrowers, p_total_loans, interest_charged, avg_cost_borrower, profitablity, loan_ppc, deliquency, risk_rate, default_rate, loss_rate, id) values(%(gender_m)s, %(term)s, %(child_flag)s, %(due_dil_type)s, %(p_rating)s, %(p_time_on_kiva)s, %(p_borrowers)s, %(p_total_loans)s, %(interest_charged)s, %(avg_cost_borrower)s, %(profitablity)s, %(loan_ppc)s, %(deliquency)s, %(risk_rate)s, %(default_rate)s, %(loss_rate)s, %(id)s)", basic)
			conn.commit()
	conn.close()
	print 'done inserting basic_info2'



# clear today_list table
def clear_today_list():
	conn = mysql.connector.connect(user = 'Qinghui', password = None, host = '127.0.0.1', database = 'test')
	cur = conn.cursor()
	cur.execute("truncate table today_list")
	conn.commit()
	conn.close()
	print 'truncate today_list'



######################################################
# main
######################################################
today_list_ids = get_old_id_list()
ae = already_exist()
insert_basic_info2(today_list_ids, ae)
#download_all_images(today_list_ids)
clear_today_list()










