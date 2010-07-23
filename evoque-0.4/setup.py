#!/usr/bin/env python
'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/setup.py $"
__revision__ = "$Id: setup.py 1154 2009-01-20 11:51:44Z mario $"

from os import curdir
from distutils.core import setup

from __init__ import __version__

setup(
    name = 'evoque',
    version = __version__,
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3',
    ],
    description = 'Evoque - managed eval-based freeform templating',
    keywords='text html xml template templating eval restricted sandbox',
    author = 'Mario Ruggier',
    author_email = 'mario@ruggier.org',
    url = 'http://evoque.gizmojo.org/',
    download_url = 'http://gizmojo.org/dist/evoque-%s.tar.gz' % (__version__),
    license = 'Academic Free License version 3.0',
    package_dir=dict(evoque=curdir),
    packages = ['evoque'],
    platforms = ['Python >= 2.4'],
    long_description=("Evoque is a lightweight full-featured generic text "
        "templating engine for python with sandbox-ability, versatility and "
        "simplicity as key feature priorities. Plus: "
        "no source file format constraints; "
        "internal processing is exclusively in unicode; "
        "dynamic template inheritance; very simple way for "
        "templates to address, call and transfer evaluation context; "
        "template managed in collections, each with own settings; "
        "small footprint, with less than 1K SLOC; extremely fast."
    ),



)
