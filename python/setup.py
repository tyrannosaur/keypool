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
   description = 'keypool: generate dict keys',

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
""",
   **kw
)     