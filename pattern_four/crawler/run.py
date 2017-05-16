import redis, json
from utils import getLinks


maxdepth = 1
depthCount = 0
host = "192.168.99.100"
port = 6379
db = 0

redisDB = redis.StrictRedis(host=host, port=port, db=db)

def crawl(page, depth):
    if depth > maxdepth:
        return
    if redisDB.exists(page):
        return
    links = getLinks(page)
    if links is None:
        return
    redisDB.set(page, json.dumps(links))
    print("Passing " + str(depth))
    for link in links:
        crawl(link, depth + 1)

crawl("http://www.uom.gr/", 0)
