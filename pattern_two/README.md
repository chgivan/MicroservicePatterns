
### Build Task1

``` sh
docker build -t chgivan/task1:latest ./task1/.
```

### Build Task2

``` sh
docker build -t chgivan/task2:latest ./task2/.
```

### Build API Gateway

``` sh
docker build -t chgivan/my_api_gateway:latest .
```

### Deploy
``` sh
docker stack deploy -c stack.yml my-app
```

### RUN
``` sh
curl 192.168.99.100/task1/
curl 192.168.99.100/task2/
```
