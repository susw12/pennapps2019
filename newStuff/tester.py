import requests
import json

auth_data = {
    'grant_type'    : 'client_credentials',
    'client_id'     : '2000765fd60031b9c843944bdb1ffa354be71141cdc5fab7',
    'client_secret' : '026449ec24a8e9be94b9dc96ee1e326c0774763b7f23d73ebe766c8b89dbcfb3',
    'scope'         : 'read_product_data'
};
# create session instance
session = requests.Session()
gsid = "10516"
auth_request = session.post("https://idfs.gs.com/as/token.oauth2", data = auth_data)
access_token_dict = json.loads(auth_request.text)
access_token = access_token_dict['access_token']

# update session headers with access token
session.headers.update({"Authorization":"Bearer "+ access_token})

request_url = "https://api.marquee.gs.com/v1/assets/gsid=" + gsid

request = session.get(url=request_url)
results = json.loads(request.text)
print(results)