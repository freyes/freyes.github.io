#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Felipe Reyes'
SITENAME = u'tty'
SITEURL = ''

TIMEZONE = 'America/Santiago'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('Jorge', 'http://frontend-jniedbalski.rhcloud.com/'),
)

DEFAULT_PAGINATION = 20

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
STATIC_PATHS = ['images']
THEME = "pelican-bootstrap3"
USE_OPEN_GRAPH = False
GOOGLE_ANALYTICS = "UA-2675698-3"
GITHUB_USER = "freyes"
BOOTSTRAP_THEME = "slate"
