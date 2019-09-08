import json
import requests
#import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

def get_news_1(queries):
    if (len(queries) < 1):
        return {}
    url1 = "https://newsapi.org/v2/everything?q="
    url2 = "&from=2019-08-08&sortBy=publishedAt&apiKey=dd6d68816cc6455c9d795dbec1f785cc"
    str = ""
    for i in range(len(queries)):
        if (i != 0):
            str += "and"
        str += '"' + queries[i] + '"'
    str = url1 + str + url2
    return json.loads(requests.get(str).content)

def get_urls_from_news(json):
    json = json['articles']
    links = []
    for item in json:
        links.append(item['url'])
    return links

print(get_urls_from_news(get_news_1(['healthcare', 'cybersecurity'])))
sia = SIA()

def get_sentiment(text):
    pol_score = sia.polarity_scores(text)
    return pol_score['compound']
