import  redis
r = redis.Redis(host='localhost', port=6379, db=0)

# a,b,c,d,e are existing items in Queue. New items f & g are added to the end of the queue.
list = ['a', 'b', 'c', 'd', 'e']
print(list)


# creata a redis list
r.rlist =[]
print(r.rlist)

# bring the list items to the redis list
r.rpush('rlist', *list) 
for i in list:
    r.rpush('rlist', i) 
print(r.lrange('rlist', 0, -1))    

   
