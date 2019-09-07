import requests, json

url='https://www.alphavantage.co/query?function=SECTOR&apikey=6J5NUW7HON53D9CU'

# in case you need a session
cd = { 'sessionid': '123..'}

#r = requests.get(url, cookies=cd)
r = requests.get(url)
sector = open("sectorData.json", "w")
sector.write(str(json.loads(r.content)))
sector.close()

url1 = "https://www.alphavantage.co/query?function=SMA&symbol=MSFT&interval=monthly&time_period=10&series_type=open&apikey=6J5NUW7HON53D9CU"
stock = open("stockData.json", "w")
s = requests.get(url1)
stock.write(str(json.loads(s.content)))
stock.close()
