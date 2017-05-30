## Fork & Join

### Build Worker

```sh
docker build -f BuildWorkerfile -t chgivan/worker:latest .
```

### Build master
``` sh
pip install pika numpy
```

### Deploy
``` sh
docker stack deploy -c stack.yml fork_join
```

### Run
``` sh
python master.py <size> <chunks> <min> <max>
```

### Undeploy
``` sh
docker stack rm fork_join
```
