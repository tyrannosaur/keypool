#!/usr/bin/env python

from keypool import __version__

try:
   from setuptools import setup
   kw = {}

except ImportError:
   from distutils.core import setup
   kw = {}

setup(
   name = 'keypool',
   packages = ['keypool'],
   version = __version__,
   description = 'Classes and helpers to generate and maintain a pool of unique integer keys.',

   author = 'Charlie Liban',
   author_email = 'charlie@tyrannosaur.ca',
   maintainer='Charlie Liban',
   maintainer_email='charlie@tyrannosaur.ca',   

   url = 'https://github.com/tyrannosaur/keypool',
   download_url = 'https://github.com/tyrannosaur/keypool/zipball/master',
   keywords = ['data structures'],
   classifiers = [
      'Programming Language :: Python',
      'License :: OSI Approved :: MIT License',
   ],

   license = 'MIT License',

   long_description = """\
Classes and helpers to generate and maintain a pool of unique integer keys.  
Priority is given to reusing freed keys rather than generating new ones.

This package is meant for situations where keys for a dict are irrelevant or
arbitrary.

Typical usage:

::

   from keypool import KeypoolDict
   items = KeypoolDict()
   
   # Assign a value with a unique, generated key
   items[items.next()] = 'hello, world'
   
   # Assign a value but capture the key
   key = items.setitem('hello again, world')
   
   # Assign anything except an integer, like a normal dict
   items['hello'] = 'world'
""",
   **kw
)     