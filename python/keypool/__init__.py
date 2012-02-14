"""Classes and helpers to generate and maintain a pool of unique integer keys.  
Priority is given to reusing freed keys rather than generating new ones.

This package is meant for situations where keys for a dict are irrelevant or
arbitrary.

Typical usage:
    
   from keypool import KeypoolDict
   items = KeypoolDict()
   
   # Assign a value with a unique, generated key
   items[items.next()] = 'hello, world'
   
   # Assign a value but capture the key
   key = items.setitem('hello again, world')
   
   # Assign anything except an integer, like a normal dict
   items['hello'] = 'world'
"""

import math
import random
import weakref

__version__ = '0.1'
__all__ = ['Keypool', 'KeypoolDict', 'DeferredKey', '__version__']

class DeferredKey(object):  
  """Gets a free key from an associated Keypool only
  when the 'key' attribute is accessed.
  """
  def __init__(self, pool):
    self._key = None
    self._pool = weakref.proxy(pool)
    
    # Remove the key from the pool when it is deleted (or goes out of scope)
    # and '_key' has been assigned
    self._autodel = True
    
  @property
  def key(self):
    """Returns a key value."""
    if self._key is None:
      self._key = self._pool.next()
    return self._key    
  
  def __del__(self):
    # Remove the key from the pool
    if self._key is not None and self._autodel:
      try:
         del self._pool[self._key]
      except weakref.ReferenceError:
         pass
  
  def __eq__(self, other):          
    try:
      if self._key is None or other._key is None:
         return False                       
      return self._pool == other._pool and self._key == other._key
    except:
      return False
  
  def __str__(self):
    return str(self.key)
  
  def __repr__(self):
    return repr(self.key)
  
  def __getattr__(self, attr):
    """ Delegate everything else to the int."""
    return getattr(self.__getattribute__('key'), attr)      

class KeypoolDict(dict):
  """Combines a dict with a Keypool for generating unique integer keys.
       
  For example, suppose some function requires a unique string internally.
  Instead of generating UUIDs or random keys, a KeypoolDict can be used.
    
    from badapi import badfunc
    from keypool import Keypool
    
    pool = KeypoolDict()
       
    def wrap_badfunc(*args, **kwargs):      
      # Get a DeferredKey. Calling str() on the key will give it a real value      
      key = str(pool.next())
      
      # Store in the dict
      pool[key] = badfunc(unique_name=key, *args, **kwargs)
      
      # Return it for later use
      return key
      
    def wrap_del_badfunc(key):      
      del pool[key]      

  The value of the key is generated when assigned to a KeypoolDict:  
      
      pool = KeypoolDict()
      keys = []
              
      # Safely GCed
      pool.next()
            
      key = pool.next()      
      keys.append(key)
            
      pool[key] = 'value'
  
      # Should be True
      key.key == keys[0].key
      
  although, be careful:
  
      key = pool.next()
      keys.append(key)
      
      # Print implicitly calls str, which generates the key value
      print(keys)
      
      # Should be True
      key.key is not None
      
  This behaviour is in the nature of a DeferredKey, since it is intended to
  proxy an int for naive functions.
  
  Note that a DeferredKey object must be used for assignment, but its value
  can be used for everything else.
  
      pool = KeypoolDict()
      key = pool.next()
   
      pool[key] = 'foo'
      pool[key.key]        # 'foo'             
      pool[key]            # 'foo'
            
      key == 0             # True
            
      del pool[0]
  """
  
  def __init__(self, *args, **kwargs):
    if 'start' in kwargs:
      start = kwargs['start']
      del kwargs['start']
    else:
      start = 0
   
    super(KeypoolDict, self).__init__(*args, **kwargs)  
    self._pool = Keypool(start=start)
  
  def next(self):
    """Return a DeferredKey object.
   The value of the object is not finalized, so next() can be called
   successively without consuming free keys."""    
    return DeferredKey(self._pool)

  def __contains__(self, key):
   if isinstance(key, DeferredKey):
      key = key.key
      
   return super(KeypoolDict, self).__contains__(key)

  def setitem(self, val):    
    key = self.next()
    self[key] = val
    return key

  def __setitem__(self, key, val):
    """Assign a value with the given key.
    If the key is not a DeferredKey object, then it is added to the normal dictionary.
    The value of the DeferredKey object is finalized on assignment.
    """
    if isinstance(key, DeferredKey):     
       # Do not allow the key to remove itself from the pool
       key._autodel = False
       key = key.key

    super(KeypoolDict, self).__setitem__(key, val)
    
  def __delitem__(self, key):      
    if isinstance(key, DeferredKey):
      key = key.key    
  
    if isinstance(key, int):  
      del self._pool[key]
      
    super(KeypoolDict, self).__delitem__(key)

class Keypool(object):
  """Generates and maintains a pool of unique integer keys.    
  Priority is given to reusing freed keys rather than generating new ones.
  
  For example:
    
    from keypool import Keypool
    
    pool = Keypool()
    a = pool.next()    # a == 0
    b = pool.next()    # a == 1
    del pool[a]        # frees key 0
    c = pool.next()    # a == 0   
  """  

  infinity = 'infinity'

  def __init__(self, start=0):        
    self._start = start
    self._free = [[start, self.infinity]]    

  @property
  def start(self):
    """Get the lowest possible key."""
    return self._start
  
  def remove(self, key):
    """Delete a key, freeing it for reuse."""
    del self[key]
    
  def next(self):
    """Return a key."""
    start, end = self._free[0]
    if start == end:
      del self._free[0]      
    else:    
      self._free[0][0] += 1    
    return start
  
  def __delitem__(self, key):  
    """Delete a key, freeing it for reuse."""
    try:
      i = self._find(key)
      self._free.insert(i, [key, key])
      
      # Merge the previous and next ranges, if they exist
      if i < len(self._free) - 1 and self._free[i+1][0] == self._free[i][1] + 1:
          self._free[i+1][0] = self._free[i][0]
          del self._free[i]
      if i > 0 and self._free[i-1][1] == self._free[i][0] - 1:
          self._free[i-1][1] = self._free[i][1]
          del self._free[i]          
    except KeyError:
      raise

  def _find(self, key):
    """Find and return the range index of a used key.
    
    If the key is free, raises a KeyError. If an invalid key
    is given, raises a ValueError.
    """    
    
    def is_used(i, key):      
      if i == 0:
        return key < self._free[i][0]
      else:    
        return key > self._free[i-1][1] and key < self._free[i][0]  
  
    if key < self.start or key > self.infinity:
      raise ValueError(u'key "%s" is invalid' % key)
  
    key = int(key)
  
    # Random pivot
    p = random.randint(0, len(self._free) - 1)
    d = 0
    max_d = math.log(len(self._free)) + 1
    
    # Stop after a reasonable depth
    while d <= max_d:
      start, end = self._free[p]      
      if is_used(p, key):            
        return p
      elif key < start:
        p = int(p/2.0)
      elif key > end:
        p += int((len(self._free) - p)/2.0)
      d += 1
    raise KeyError(u'key "%s" is not in use' % key)    