Classes and helpers to generate and maintain a pool of unique integer keys.  
Priority is given to reusing freed keys rather than generating new ones.

This package is meant for situations where keys for a dict are irrelevant or
arbitrary.

The basics:

   from keypool import KeypoolDict
   items = KeypoolDict()
   
   # Assign a value with a unique, generated key
   items[items.next()] = 'hello, world'
   
   # Assign a value but capture the key
   key = items.setitem('hello again, world')
   
   # Assign anything except an integer, like a normal dict
   items['hello'] = 'world'

For example, let's say you're wrapping a timer function in some horrible API:

   def timer(unique_name, **kwargs):
      ...
      
and each active timer needs to be stored. Usually a timestamp or uuid will
suffice for this type of problem:

   import time
   
   timers = {}
   
   def create_timer(**kwargs):         
      key = str(time.time())
      timers[key] = timer(unique_name=key, **kwargs)
      return key

   # Oops, the loop is iterating faster than time.time's precision   
   keys = [create_timer(...) for i in xrange(0, 10)]
   
   # All keys are identical
   assert not all([keys[0] == key for key in keys])     
      
A KeypoolDict will generate unique integer keys that are reused when deleted:

   from keypool import KeypoolDict
   from operator import delitem
   
   timers = KeypoolDict()
   
   def create_timer(**kwargs):
      key = timers.next()
      timers[key] = timer(unique_name=key, **kwargs)
      return key
   
   keys = [create_timer(...) for i in xrange(0, 10)]
   
   # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   print(keys)   
   
   # No keys are identical
   assert all([x == y for x,y in zip(sorted(set(keys)), sorted(keys))])
   
   # Delete all the items
   [delitem(timers, key) for key in timers.keys()]
   
   # The old keys are now reused   
   keys = [create_timer(...) for i in xrange(0, 10)]
   
   # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   print(keys)   