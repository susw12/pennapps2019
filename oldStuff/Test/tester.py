# GS Quant documentation available at:
# https://developer.gs.com/docs/gsquant/guides/getting-started/

import datetime, json, csv, mysql.connector

from gs_quant.data import Dataset
from gs_quant.session import GsSession, Environment

info = {}
with open('marquee_config.json', "r") as file:
	info = json.load(file)

GsSession.use(Environment.PROD, '74d4f25c0	33e4bd7ad6909ca40f6ad8d', '15c2a007595b37787456949fd6bb35aa23c77b3495ffe449e2c7476f0d7e87f6', scopes=GsSession.Scopes.get_default())

ds = Dataset('USCANFPP_MINI')
data = ds.get_data(datetime.date(2017, 1, 15), datetime.date(2018, 1, 15), gsid=["75154", "193067", "194688", "902608", "85627"])
# print(data.to_csv()) # peek at first few rows of data
	
data = data.values.tolist()

sql_config = {}

with open('sql_config.json', "r") as file:
	sql_config = json.load(file)

conn = mysql.connector.connect(**sql_config)
cursor = conn.cursor()

def addrow(r):
	str = "insert into csvdb (a, b, c, d, e, f)\n \
	values(%s, %s, %s, %s, %s, %s)"
	try:
		cursor.execute(str, tuple(r))
	except mysql.connector.Error as error:
		print("db error:", error)

for row in data:
	addrow(row)
	
conn.commit()
conn.close()
cursor.close()

'''
table csvdb (
	a varchar(50),
	b varchar(50),
	c varchar(50),
	d varchar(50),
	e varchar(50),
	f varchar(50)
)
'''