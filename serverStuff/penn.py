from flask import Flask, request, render_template, jsonify, json, redirect, url_for
from werkzeug.utils import secure_filename
import os, sys, random, json, requests, datetime, csv, time, intrinio_sdk, numpy as np, pandas as pd
from json import dumps
import mysql.connector #pip install mysql-connector

from gs_quant.data import Dataset
from gs_quant.session import GsSession, Environment

from intrinio_sdk.rest import ApiException
from pprint import pprint, pformat

from gensim.summarization import keywords

# import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
#boilerpipe
app = Flask(__name__)

def read_config(filename):
	with open(filename, "r") as file:
		return json.load(file)

sql_config = read_config('sql_config.json')
	
#DONE
def login(username, password):
	str = "select * from business_users where uname=%s and pword=%s"
	ext = (username, password)
	records = []
	try:
		conn = mysql.connector.connect(**sql_config)
		cursor = conn.cursor(buffered=True)
		cursor.execute(str, ext)
		conn.commit()
		records = cursor.fetchall()
	except mysql.connector.Error as error:
		print("db error:", error)
	finally:
		conn.close()
		cursor.close()
	return records

#DONE
def unused_login(username, password):
	res = login(username, password)
	if (len(res) > 0):
		return False
	else:
		return True

#DONE
def register(username, password, dbname, nodup=True):
	str = "insert into %s (uname, pword)\n \
	values(%s, %s)"
	ext = (dbname, username, password)
	res = unused_login(username, password, dbname)
	print(res)
	if (not res):
		return
	try:
		conn = mysql.connector.connect(**sql_config)
		cursor = conn.cursor()
		cursor.execute(str, ext)
		conn.commit()
	except mysql.connector.Error as error:
		print("db error:", error)
	finally:
		conn.close()
		cursor.close()
		
def register_business(username, password, business_name, business_desc, image, location, email, website, bkeys, nodup=True):
	str = "insert into business_users (uname, pword, bname, bdesc, image, location, email, website, bkeys)\n \
	values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	ext = (username, password, business_name, business_desc, image, location, email, website, bkeys)
	res = unused_login(username, password)
	if (not res and nodup):
		return
	try:
		conn = mysql.connector.connect(**sql_config)
		cursor = conn.cursor()
		cursor.execute(str, ext)
		conn.commit()
	except mysql.connector.Error as error:
		print("db error:", error)
	finally:
		conn.close()
		cursor.close()
		
def get_keywords(username, password):
	str = "select * from business_users where uname = %s and pword = %s"
	ext = (username, password)
	res = 0
	try:
		conn = mysql.connector.connect(**sql_config)
		cursor = conn.cursor(buffered=True)
		cursor.execute(str, ext)
		conn.commit()
		res = cursor.fetchall()[0][8]
	except mysql.connector.Error as error:
		print("db error:", error)
	finally:
		conn.close()
		cursor.close()
	print(res)
	return res
	
# get_keywords("i", "h")
# get_keywords("i", "i")
# sys.exit(0)
		
# register_business("a", "b", "c", "d", "e", "f", "g", "h", "i")

'''
# gsids = ['75154', '193067', '194688', '902608', '85627', '13901', '150407', '161467', '85072', '82598', '86372', '11896', '230958', '177256', '49154', '76605', '173578', '85914', '193324', '75100', '149756', '213305', '79758', '69796', '81116', '202271', '79145', '84275', '183269', '76226', '18163', '80791', '152963', '197235', '227284', '222946', '85631', '25022', '61621', '59010', '902704', '216587', '901237', '80286', '77659', '15579', '53613', '16600', '75573', '216722', '46578', '75573', '53065', '84769', '13936', '46922', '905632', '13936', '193155', '91556', '64064', '79265', '151048', '176665', '46886', '183414', '70500', '16432', '905632', '173578', '86196', '11308', '55976', '188804', '226278', '26825', '183269', '172890', '905288', '29209', '188329', '10516', '75607', '18729', '16678', '44644', '223416', '82598', '26403', '91556', '59248', '78975', '903917', '78045', '12490', '40539', '148401', '17750', '198025', '10696', '22293', '66384', '85517', '217708', '79145', '85631', '86356', '905255', '14593', '85072']
gsids = ["75154", "193067", "194688", "902608", "85627"]
#DONE	
def get_marquee(datid, gsids, begin=datetime.date(2019, 1, 15), end=datetime.date(2019, 9, 8), store_db=False, csv=False):
	info = read_config('marquee_config.json')

	GsSession.use(Environment.PROD, '48d117ad4e9045b8a4ae357972acf9dd', 'e14e42f89cb87deeb5eee6237ac7ebcb5bd935a9b27b838abcdf4307b326fe8d', scopes=GsSession.Scopes.get_default())

	ds = Dataset(datid)
	data = ds.get_data(gsid=gsids)
	
	# print(data.to_csv()) # peek at first few rows of data
		
	data = data.values.tolist()
	print(data)
	
	npa = np.array(data)
	auth_data = {
		'grant_type'    : 'client_credentials',
		'client_id'     : '48d117ad4e9045b8a4ae357972acf9dd',
		'client_secret' : 'e14e42f89cb87deeb5eee6237ac7ebcb5bd935a9b27b838abcdf4307b326fe8d',
		'scope'         : 'read_product_data'
	};
	# create session instance
	session = requests.Session()
	auth_request = session.post("https://idfs.gs.com/as/token.oauth2", data = auth_data)
	access_token_dict = json.loads(auth_request.text)
	access_token = access_token_dict["access_token"]
	# update session headers with access token
	session.headers.update({"Authorization":"Bearer "+ access_token})
	
	def secDat(gsid):
		request_url0 = "https://api.marquee.qs.com/v2/assets/data?gsid=" + gsid
		request = session.get(url=request_url0)
		results = json.loads(request.text)
		return results["results"][0]["classifications"]["gicsSector"]
		
	def namDat(gsid):
		request_url0 = "https://api.marquee.qs.com/v2/assets/data?gsid=" + gsid
		request = session.get(url=request_url0)
		results = json.loads(request.text)
		return results["results"][0]["name"]
		
	def ticDat(gsid):
		request_url0 = "https://api.marquee.qs.com/v2/assets/data?gsid=" + gsid
		request = session.get(url=request_url0)
		results = json.loads(request.text)
		return results["results"][0]["shortName"]
	
	# print(pd.DataFrame({'first': npa[:, 0], 'third': npa[:, 2], 'date': npa[:, 5]}))

	if store_db:
		sql_config = {}

		with open('sql_config.json', "r") as file:
			sql_config = json.load(file)

		conn = mysql.connector.connect(**sql_config)
		cursor = conn.cursor()

		def addrow(r):
			r.append(0)
			r.append(0)
			r.append(0)
			
			# shift elements right 3
			for i in range(6):
				r[i + 3] = r[i]
				
			r[0] = secDat(r[5])
			r[1] = namDat(r[5])
			r[2] = ticDat(r[5])
			str = "insert into business_users (a, b, c, d, e, f, g, h, i)\n \
			values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			try:
				cursor.execute(str, tuple(r))
			except mysql.connector.Error as error:
				print("db error:", error)

		for row in data:
			addrow(row)
			
		
		conn.commit()
		conn.close()
		cursor.close()
		
	# data comes already parsed

	
	return data
	
get_marquee('USCANFPP_MINI', gsids, store_db=True)
'''
#DUH
def parse_marquee(data): # just for consistency
	return data
	
#DONE
def get_alphavantage():
	info = read_config('alpha_config.json')

	url='https://www.alphavantage.co/query?function=SECTOR&apikey=' + info['key']

	# in case you need a session
	cd = { 'sessionid': '123..'}

	#r = requests.get(url, cookies=cd)
	r = requests.get(url).content #sector

	url = "https://www.alphavantage.co/query?function=SMA&symbol=MSFT&interval=monthly&time_period=10&series_type=open&apikey="  + info['key']
	s = requests.get(url).content #stock

	return r, s
	
#DONE
def parse_alphavantage(sector, stock):
	a = []
	w = json.loads(sector)
	for item in w:
		b = []
		for token in w[item]:
			b.append([token, w[item][token]])
		a.append(b)
	a = a[1:] #ignore metadata
	b = []
	x = json.loads(stock)['Technical Analysis: SMA']
	for item in x:
		b.append([item, x[item]['SMA']])
	return a, b

## DONE
# def get_intrinio(company):
	# info = read_config('intrinio_config.json')
		
	# intrinio_sdk.ApiClient().configuration.api_key['api_key'] = info['key']
	
	# company_api = intrinio_sdk.CompanyApi()
	# security_api = intrinio_sdk.SecurityApi()

	# identifier = company # str | A Security identifier (Ticker, FIGI, ISIN, CUSIP, Intrinio ID)
	# start_date = '2018-01-01' # date | Return prices on or after the date (optional)
	# end_date = '2019-01-01' # date | Return prices on or before the date (optional)
	# frequency = 'daily' # str | Return stock prices in the given frequency (optional) (default to daily)
	# page_size = 100 # int | The number of results to return (optional) (default to 100)
	# next_page = '' # str | Gets the next page of data from a previous API call (optional)
	
	# try:
		# global companyInfo, stockInfo
		# companyInfo = company_api.get_company(identifier)
		# stockInfo = security_api.get_security_stock_prices(identifier, start_date=start_date, end_date=end_date, frequency=frequency, page_size=page_size, next_page=next_page)
	# except ApiException as e:
	  # print("U dun goofed")
	# return companyInfo, stockInfo
	
## AWAITING FURTHER INSTRUCTIONS
# def parse_intrinio(company, stock):
	## so far, company info is not used
	## and we don't know what we want with stock info
	# return company, stock

def get_news_1(queries):
	if (len(queries) < 1):
		return {}
	url1 = "https://newsapi.org/v2/everything?q="
	url2 = "&from=2019-08-08&sortBy=publishedAt&apiKey=dd6d68816cc6455c9d795dbec1f785cc"
	str = ""
	for i in range(len(queries)):
		if (i != 0):
			str += "and"
		str += '\"' + queries[i] + '\"'
	str = url1 + str + url2
	return json.loads(requests.get(str).content)
	
def get_urls_from_news(json):
	json = json['articles']
	links = []
	for item in json:
		links.append(item['url'])
	return links
	
def boil_the_text(url):
	return url
    # link = 'http://boilerpipe-web.appspot.com/extract?url=' + url + '&output=text'
    # return Extractor(extractor='ArticleExtractor', url=url).getText()
	
def get_news_objects():
	#format, kevin, sujay, whatever
	return {}
	
# print(get_urls_from_news(get_news_1(['healthcare', 'cybersecurity'])))

# x = get_marquee('USCANFPP_MINI', ["75154", "193067", "194688", "9002608", "85627"], datetime.date(2017, 1, 15), datetime.date(2018, 1, 15), False, True)
# print(x)

# a, b = get_alphavantage()
# a, b = parse_alphavantage(a, b)
# print(a)
# print(b)

# c, d = get_intrinio('MSFT')
# c, d = parse_intrinio(c, d)
# print(c)
# print(d)

sia = SIA()

def get_sentiment(text):
	pol_score = sia.polarity_scores(text)
	return pol_score['compound']
	
#DONE
#Home
@app.route('/')
def root():
	return render_template('index.html')
	
#DONE?
@app.route('/login')
def logpage():
	return render_template('login.html')
	
@app.route('/register')
def regpage():
	return render_template('register.html')

@app.route('/register_business', methods = ["POST"])
def regbusiness():
	js = request.get_json(force=True)
	register_business(js['uname'], js['pword'], js['bname'], js['bdesc'], js['image'], js['location'], js['email'], js['website'], js['bkeys'])
	return '1'
	
@app.route('/login_business', methods = ["POST"])
def logbusiness():
	js = request.get_json(force=True)
	login(js['uname'], js['pword'])
	return '1'

#AWAIT
@app.route('/login_investor', methods = ["POST"])
def loginvestor():
	js = request.get_json()
	# register(json['uname'], json['pword'], json['bname'], json['bdesc'], json['image'], 'investor_users')

#DONE
@app.route('/page1')
def page1():
	return render_template('page1.html')

_localst = {}

#AWAIT news acquirement
@app.route('/page1_search', methods = ["POST"])
def page1_search():
	js = request.get_json()
	query = js['query']
	sector = js['sector']
	uname = js['uname']
	pword = js['pword']
	query = "query, quest"
	sector = "technology"
	uname = "a"
	pword = "b"
	query = query.split(',')
	
	query.append(sector)
	
	news = get_news_1(query)
	
	#title, url, snippet
	a = []
	for item in news['articles']:
		a.append([item['title'], item['url'], item['description']])
		
	_localst[uname + pword] = [a, query, sector]
	return redirect(url_for('page2'))
	
	#get news sites
	#for each one, get its keywords (and first element should be its url)
	#for each of those, return the ones that correspond to query

# page1_search()

#DONE
@app.route('/page2')
def page2():
	return render_template('page2.html')
	
#AWAIT acquisition of news
@app.route('/page2_info')
def page2_info():
	uname = js['uname']
	pword = js['pword']
	a, query, sector = _localst.pop([uname + pword])
	
	sum = 0
	cnt = 0
	for item in a:
		item = boil_the_text(item)
		sum += get_sentiment(item)
		cnt++
	
	avg = sum / cnt
	
	query.pop(-1)
	return jsonify({"pages": a, "queries": query, "average": avg, "sector": sector})
	#this one needs the news sites (like page1) and the search results

#AWAIT news
@app.route('/page2_search', methods = ["POST"])
def page2_search():
	js = request.get_json()
	query = js['query']
	sector = js['sector']
	uname = js['uname']
	pword = js['pword']
	query = "query, quest"
	sector = "technology"
	uname = "a"
	pword = "b"
	query = query.split(',')
	
	query.append(sector)
	
	news = get_news_1(query)
	
	#title, url, snippet
	a = []
	for item in news['articles']:
		a.append([item['title'], item['url'], item['description']])
		
	_localst[uname + pword] = [a, query, sector]
	return redirect(url_for('page2'))

#DONE
@app.route('/page3')
def page3():
	return render_template('page3.html')

#AWAIT
@app.route('/page3_update', methods = ["POST"])
def page3_update():
	json = request.get_json()
	clicked = json['clicked']
	#return the list of stuff and stuff

#AWAIT
@app.route('/profile/<name>')
def profile(name):
	return 1 #stuff
	
@app.route('/map_page')
def get_map_page():
	return render_template('map.html')

@app.route('/map_info')
def get_map():
	list = []
	res = []
	try:
		conn = mysql.connector.connect(**sql_config)
		cursor = conn.cursor()
		cursor.execute('select * from business_users')
		res = cursor.fetchall()
		conn.commit()
	except mysql.connector.Error as error:
		print("db error:", error)
	finally:
		conn.close()
		cursor.close()
	for item in res:
		list.append([item[0], item[5]]) #username, location
	return jsonify(list)
	
states = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}

app.run(debug=True)
'''
table <generic>_users (
	uname varchar(200),
	pword varchar(200),
	bname varchar(200),
	bdesc varchar(2000),
	image varchar(200),
	location varchar(200),
	email varchar(200),
	website varchar(200),
	bkeys varchar(200)
)

alphavantage:
Rank A: Real-Time Performance
Rank B: 1 Day Performance
Rank C: 5 Day Performance
Rank D: 1 Month Performance
Rank E: 3 Month Performance
Rank F: Year-to-Date (YTD) Performance
Rank G: 1 Year Performance
Rank H: 3 Year Performance
Rank I: 5 Year Performance
Rank J: 10 Year Performance
'''