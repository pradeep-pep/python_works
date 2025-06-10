import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Set a key
r.set('mykey', 'Hello Redis!')

# Get the key
value = r.get('mykey')
print(value.decode('utf-8'))  # Output: Hello Redis!
