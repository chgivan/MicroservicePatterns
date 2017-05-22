import redis, time

host = "192.168.99.100"
port = 6379
db = 0

redisDB = redis.StrictRedis(host=host, port=port, db=db)

for key in redisDB.keys("*"):
    print(str(key) + ":" + str(redisDB.get(key)))
    print("New Page")
