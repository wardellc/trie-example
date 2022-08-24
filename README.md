docker run -p 6379:6379 redis


python3 -m venv redis-virtualenv
source redis-virtualenv/bin/activate
python3 -m pip install redis
python3 main.py
deactivate


P -> Pear -> 1
Pe -> Pear -> 1
etc...
where 1 is weight (frequency of the word)

Note: weights will increase everytime you run this script as it run the populate function each time.