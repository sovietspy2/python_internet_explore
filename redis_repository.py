import redis
import logging

# Replace these values with your Redis server details
host = 'localhost'
port = 6379  # Default Redis port
db = 0      # Default Redis database

# Create a Redis connection
r = redis.StrictRedis(host=host, port=port, db=db)

# Enqueue (Push) elements to the queue
def queue_put(queue_name, item):
    r.lpush(queue_name, item)
    #logging.debug("added item to redis")

# Dequeue (Pop) an element from the queue
def queue_get(queue_name):
    item = r.rpop(queue_name)
    #logging.debug("got item from redis")
    return item.decode() if item else None

def add_to_set(set_name, item):
    r.sadd(set_name, item)

# Check if an item is in the set (contains operation)
def set_contains(set_name, item):
    return bool(r.sismember(set_name, item))

