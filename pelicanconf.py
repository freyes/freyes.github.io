#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Felipe Reyes'
SITENAME = u'Felipe Reyes'
SITEURL = 'http://freyes.github.io'

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
    ('@niedbalski', 'http://www.metaklass.org/'),
    ("Monkey Project", "http://monkey-project.com/"),
)

DEFAULT_PAGINATION = 20
DISPLAY_PAGES_ON_MENU = True
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
STATIC_PATHS = ['images', 'CNAME']
THEME = "iris"
USE_OPEN_GRAPH = False
GOOGLE_ANALYTICS = GOOGLE_ANALYTICS_CODE ="UA-2675698-3"
GOOGLE_ANALYTICS_DOMAIN = "freyes.github.io"
GOOGLE_ANALYTICS_DOMAIN_UP = False
GITHUB_USER = "freyes"
BOOTSTRAP_THEME = "slate"
EMAIL = "freyes@tty.cl"
