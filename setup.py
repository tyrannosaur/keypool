#!/usr/bin/env python

from distutils.core import setup
from web import __version__

setup(name='web.py',
      version=__version__,
      description='keypool: generate dict keys',
      author='Charlie Liban',
      author_email='charlie@tyrannosaur.ca',
      maintainer='Charlie Liban',
      maintainer_email='charlie@tyrannosaur.ca',
      url='https://github.com/tyrannosaur/keypool',
      packages=['keypool'],
      long_description="Classes and helpers to generate and maintain a pool of unique integer keys.",
      license="MIT License",
      platforms=["any"],
     )