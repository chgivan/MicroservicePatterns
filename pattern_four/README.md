
### Deploy

```sh
    docker build -t crawler:latest ./crawler/.
```

### Deploy

```sh
    docker stack deploy -c stack.yml my_crawler
```

## Run
```sh
    python crawler/run.py www.uom.gr 1
```

## See Database
```sh
    python watcher.py
```
