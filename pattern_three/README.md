### Build filter
''' sh
docker build -t chgivan/filter:latest ./filter/.
'''

### Deploy
''' sh
docker stack deploy -c stack.yml pipes_filters
'''

### RUN
''' sh
python pipe1.py
python pipe2.py
'''
