import redis, json, urllib.request
from utils import LinkHTMLParser


depth = 5
depthCount = 0
host = "192.168.99.100"
port = 6379
db = 0

redisDB = redis.StrictRedis(host=host, port=port, db=db)

def crawl(my_page):
    if redisDB.exists(my_page):
        return
    
    try:
        with urllib.request.urlopen('http://www.uom.gr/') as response:
             parser = LinkHTMLParser()
             parser.feed(str(response.read()))
             parser.close()
             global new_links
             new_links = parser.links
    except Exception as e:
        print (str(e))
        return
    for page in input_pages[my_page]:
        new_links.append(page)
    redisDB.set(my_page, json.dumps(new_links))
    for page in new_links:
        crawl(page)

crawl("index")

print("Input Pages")
print(input_pages)
