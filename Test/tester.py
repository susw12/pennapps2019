import os, sys, random, json, requests

marquee_config = {}

with open('marquee_config.json', "r") as file:
    marquee_config = json.load(file)

marquee_config['grant_type'] = 'client_credentials'
# marquee_config['scope'] = ''

print(marquee_config)

_url = 'https://api.marquee.gs.com	/v1/data/dimensions/USCANFPP_MINI'

session = requests.Session()

auth_request = session.post("https://idfs.gs.com/as/token.oauth2", data = marquee_config)
access_token_dict = json.loads(auth_request.text)
access_token = access_token_dict["access_token"]

session.headers.update({"Authorization":"Bearer "+ access_token})

request = session.get(url=_url)
results = json.loads(request.text)

print(results)

print(requests.get(url = _url, params = marquee_config))

'''
table <generic>_users (
    uname varchar(50),
    pword varchar(50)
)
'''