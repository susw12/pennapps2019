import json
import requests, time
#import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
# from boilerpipe.extract import Extractor
from gensim.summarization import keywords

def get_news_1(queries):
    if (len(queries) < 1):
        return {}
    url1 = "https://newsapi.org/v2/everything?q="
    url2 = "&from=2019-08-08&sortBy=publishedAt&apiKey=9d0ad847ada9474385d8cf0ce1ae4719"
    str = ""
    for i in range(len(queries)):
        if (i != 0):
            str += "and"
        str += '"' + queries[i] + '"'
    str = url1 + str + url2
    return json.loads(requests.get(str).content)
	
print(json.dumps(get_news_1(['query', 'quest'])))

def get_urls_from_news(json):
    json = json['articles']
    links = []
    for item in json:
        links.append(item['url'])
    return links

sia = SIA()

def get_sentiment(text):
    pol_score = sia.polarity_scores(text)
    return pol_score['compound']

def boil_the_text(url):
    link = 'http://boilerpipe-web.appspot.com/extract?url=' + url + '&output=text'
    return Extractor(extractor='ArticleExtractor', url=url).getText()

link = get_urls_from_news(get_news_1(['healthcare', 'cybersecurity']))
text = boil_the_text(link[0])

print(keywords(str(text)).split('\n'))

for i in range(15):
    text = str(boil_the_text(link[i]))
    print(text[:404])
    print(get_sentiment(text))  