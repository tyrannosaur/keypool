# keypool

`keypool` is a library to generate and maintain a pool of unique integer keys. Priority is given to reusing
freed keys rather than generating new ones.

This package is meant for situations where keys for a dict are irrelevant or
arbitrary.

## Installation

### Python

Only `setuptools` and Python 2.6+ are required. Type `python setup.py install` to install. 
If you want to run the tests, ensure `nose` is installed with `easy_install -U nose`.

### JavaScript

The JavaScript version requires no dependencies or special interpreters.

## The basics

### Python
```python
      from keypool import KeypoolDict
      items = KeypoolDict()
      
      # Assign a value with a unique, generated key
      items[items.next()] = 'hello, world'
      
      # Assign a value but capture the key
      key = items.setitem('hello again, world')
      
      # Assign anything except an integer, like a normal dict
      items['hello'] = 'world'
```

When an item is deleted, its key is freed for reuse:

```python
      from keypool import KeypoolDict
      items = KeypoolDict()

      # Add some items
      keys = [items.setitem(word) for word in ['aardvark', 'baboon', 'crocodile']]

      # [0, 1, 2]
      print(keys)

      # Delete 0
      del items[keys[0]]

      # Add a new item
      key = items.setitem('dragonfly')

      # 0 (as opposed to 3)
      print(key)             
```

### JavaScript

```javascript
     var items = keyPool();
     
     // Assign a value with a unique integer.
     // The key is immediately generated, unlike in Python
     items[items.newKey()] = 'hello, world';
     
     // Assign a value but capture the key
     var key = items.set('hello again, world');
     
     // Assign anything except an integer to the internal object
     items['hello'] = 'world';
          
     items.del(key);      // key 1 is removed and the next free key will be 1
     items.del('hello');  // a key outside the pool is removed
```

## Examples

Let's say you're wrapping a timer function in some horrible API:

```python
      def timer(unique_name, **kwargs):
            ...
```
            
and each active timer needs to be stored for efficient lookup (i.e. a dict).
Usually a timestamp or uuid will suffice for this type of problem:

```python
      import time
      
      timers = {}
      
      def create_timer(**kwargs):                  
            key = str(time.time())
            timers[key] = timer(unique_name=key, **kwargs)
            return key

      keys = [create_timer(...) for i in xrange(0, 10)]
```

Oops, the loop is iterating faster than ``time.time``'s precision and
thus all keys are identical:

```python      
      # [1310422700.9400001, 1310422700.9400001, 1310422700.9400001, 
      #  1310422700.9400001, 1310422700.9400001, 1310422700.9400001, 
      #  1310422700.9400001, 1310422700.9400001, 1310422700.9400001, 
      #  1310422700.9400001]
      print(keys)
      
      assert not all([keys[0] == key for key in keys])        
```
            
A KeypoolDict solves this problem in a cleaner fashion with unique interger keys:

```python
      from keypool import KeypoolDict
      from operator import delitem
      
      timers = KeypoolDict()
      
      def create_timer(**kwargs):
            key = timers.next()
            timers[key] = timer(unique_name=key, **kwargs)
            return key
      
      keys = [create_timer(...) for i in xrange(0, 10)]
```

No keys are identical now!

```python     
      # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      print(keys)      
      
      assert all([x == y for x,y in zip(sorted(set(keys)), sorted(keys))])
```

Keys are also reused when deleted, so arbitrarily increasing values are mostly avoided:

```python
      # Delete all the items
      [delitem(timers, key) for key in timers.keys()]
      
      # The old keys are now reused      
      keys = [create_timer(...) for i in xrange(0, 10)]
      
      # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      print(keys)      
```