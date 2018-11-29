import crawler
import pagerank
import redis
import json
import pprint
import os


bot = crawler.crawler(None, "urls.txt")
bot.crawl(depth=1)
page_rank = pagerank.page_rank(bot._links)
inverted_index = bot.get_inverted_index()
resolved_inverted_index = bot.get_resolved_inverted_index()
lexicon = bot._doc_id_cache
url_lexicon = bot._url_lexicon

# convert dictionary to json string data and convert all sets in values to list form
json_page_rank = json.dumps(dict(page_rank))   
json_inverted_index = {k:list(v) for k,v in inverted_index.items()}
json_inverted_index = json.dumps(json_inverted_index) 
json_resolved_inverted_index = {k:list(v) for k,v in resolved_inverted_index.items()}
json_resolved_inverted_index = json.dumps(json_resolved_inverted_index)   
json_lexicon = json.dumps(dict(lexicon))
    
# store all data to redis database
# redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
# redis_db.set('page_rank',json_page_rank)
# redis_db.set('inverted_index',json_inverted_index)
# redis_db.set('resolved_inverted_index',json_resolved_inverted_index)
# redis_db.set('url_id_lexicon',json_lexicon)

readable_page_rank = {}
for key,value in page_rank.items():
    url = url_lexicon[key]
    url = str(url)
    readable_page_rank[url]=value
    
readable_page_rank = (sorted(dict(readable_page_rank).iteritems(),key=lambda kv: kv[1], reverse=True))
pp = pprint.PrettyPrinter(indent=1)
readable_page_rank.insert(0,("url","PageRank scores in descending order"))
pp.pprint(readable_page_rank)

