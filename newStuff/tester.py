import json
import requests
# GS Quant documentation available at:
# https://developer.gs.com/docs/gsquant/guides/getting-started/

import datetime, json, csv, mysql.connector

from gs_quant.data import Dataset
from gs_quant.session import GsSession, Environment

GsSession.use(Environment.PROD, '74d4f25c033e4bd7ad6909ca40f6ad8d', 'd698e64f7c7d549225be2b2e4b1048e6e74aa2e7469d9ec37aae3bf98d7c9abc', scopes=GsSession.Scopes.get_default())

ds = Dataset('USCANFPP_MINI')
data = ds.get_data(datetime.date(2017, 1, 15), datetime.date(2018, 1, 15), gsid=["75154", "193067", "194688", "902608", "85627"])
# print(data.to_csv()) # peek at first few rows of data
	
data = data.values.tolist()

auth_data = {
    'grant_type'    : 'client_credentials',
    'client_id'     : '74d4f25c033e4bd7ad6909ca40f6ad8d',
    'client_secret' : 'd698e64f7c7d549225be2b2e4b1048e6e74aa2e7469d9ec37aae3bf98d7c9abc',
    'scope'         : 'read_product_data'
};
# create session instance
session = requests.Session()
gsid = "id"
auth_request = session.post("https://idfs.gs.com/as/token.oauth2", data = auth_data)
access_token_dict = json.loads(auth_request.text)
access_token = access_token_dict["access_token"]

# update session headers with access token
session.headers.update({"Authorization":"Bearer "+ access_token})
request_url0 = "https://api.marquee.qs.com/v2/assets/data?gsid=" + gsid

request = session.get(url=request_url0)
results = json.loads(request.text)
print(results["results"][0]["classifications"]["gicsSector"])

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
print(r)