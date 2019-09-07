from __future__ import print_function
import time
import intrinio_sdk
from intrinio_sdk.rest import ApiException
from pprint import pprint, pformat
import json

intrinio_sdk.ApiClient().configuration.api_key['api_key'] = 'OjMwMDZjOWUwNjMzY2FlZjhlNjdkY2NkMTMzZmFhZDhj'
company_api = intrinio_sdk.CompanyApi()

identifier = '$SIC.20' # str | A Security identifier (Ticker, FIGI, ISIN, CUSIP, Intrinio ID)

security_api = intrinio_sdk.SecurityApi()

#identifier = 'AAPL' # str | A Security identifier (Ticker, FIGI, ISIN, CUSIP, Intrinio ID)
#start_date = '2018-01-01' # date | Return prices on or after the date (optional)
#end_date = '2019-01-01' # date | Return prices on or before the date (optional)
#frequency = 'daily' # str | Return stock prices in the given frequency (optional) (default to daily)
#page_size = 100 # int | The number of results to return (optional) (default to 100)
#next_page = '' # str | Gets the next page of data from a previous API call (optional)

try:
  companyInfo = company_api.get_company(identifier)
  #stockInfo = security_api.get_security_stock_prices(identifier, start_date=start_date, end_date=end_date, frequency=frequency, page_size=page_size, next_page=next_page)
  f = open("Company Info.json", "w")
  pprint(companyInfo)
  f.write(str(pformat(companyInfo)))
  #s = open("Stock Info.json", "w")
  #s.write(str(pformat(stockInfo)))
  f.close() 
  #s.close()

except ApiException as e:
  print("U dun goofed")
    
