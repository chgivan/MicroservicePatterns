
### Deploy

'''sh
    docker stack deploy -c stack.yml my_crawler
'''

## Run
'''sh
    import redis
    r = redis.StrictRedis(host='192.168.99.100', port=6379, db=0)
'''
