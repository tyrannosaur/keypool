"""nose tests"""
from keypool import KeypoolDict, Keypool
from operator import delitem
import random

MAX_ITER = 10

def assert_unique(keys):
   assert all([x == y for x,y in zip(sorted(set(keys)), sorted(keys))])
    
def test_init():
   pool = Keypool(start=0)
   dict = KeypoolDict()   
   assert dict == {}
   
   del pool
   del dict
   
   dict = KeypoolDict(hello='world')
   assert dict == {'hello' : 'world'}
   
   del dict
   
   dict = KeypoolDict([('start', 'world')], start=100)
   assert dict == {'start' : 'world'}
   assert dict._pool.start == 100
   
def test_keygen():
   pool = Keypool(start=0)
   dict = KeypoolDict()
   
   for i in xrange(0, MAX_ITER):      
      k1 = pool.next()
      k2 = dict.next()
      print k1
      print k2

def test_quick_allocate():   
   items = KeypoolDict()
   min = 2
   max = 10
   
   for i in xrange(0, MAX_ITER):
      rand = random.randint(min, max)
      keys = [items.setitem(i) for i in xrange(0, rand)]    
      assert_unique(keys)
    
def test_reuse(min_items=2, max_items=1000):
   items = KeypoolDict()
   
   for i in xrange(0, MAX_ITER):
      rand = random.randint(min_items, max_items)
      keys = [items.setitem(i) for i in xrange(0, rand)]

      # No keys are identical
      assert_unique(keys)

      # Delete all the items
      [delitem(items, key) for key in items.keys()]

      # The old keys are now reused         
      keys2 = [items.setitem(i) for i in xrange(0, rand)]
      
      assert keys == keys2
      assert_unique(keys)
      
      [delitem(items, key) for key in items.keys()]

def test_contains(min_items=2, max_items=1000):
   items = KeypoolDict()
        
   for i in xrange(0, MAX_ITER):
      rand = random.randint(min_items, max_items)
      keys = [items.setitem(i) for i in xrange(0, rand)]

      assert all([key in items for key in keys])

def test_no_intermediate_assignment():
   items = KeypoolDict()
   items[items.next()] = 'a'
   items[items.next()] = 'b'
   items[items.next()] = 'c'
   
   del items[0]  
   
   assert 0 not in items      
   assert 1 in items
   assert 2 in items
   
   items[items.next()] = 'd'
   
   assert 0 in items
   assert items[0] == 'd'
   