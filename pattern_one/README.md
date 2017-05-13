## Data Parallelism

$ docker build -t chgivan/pattern_one_worker:latest -f BuildWorkerfile .

# join & fork
- master -> rabbitmq(join) -> worker ->  rabbitmq(reduce) -> master
