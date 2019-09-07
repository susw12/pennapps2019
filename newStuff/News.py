import requests
import json
print(requests.get("https://newsapi.org/v2/everything?q=\"healthcare\"and\"cybersecurity\"&from=2019-08-07&sortBy=publishedAt&apiKey=dd6d68816cc6455c9d795dbec1f785cc").content)