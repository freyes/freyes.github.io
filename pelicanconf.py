#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Felipe Reyes'
SITENAME = u"TTY.cl"
SITESUBTITLE = "Random thoughts and knowledge"
SITEURL = "http://tty.cl"

TIMEZONE = 'America/Santiago'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_DOMAIN = "http://tty.cl/"
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/%s.atom.xml"
TAG_FEED_ATOM = "feeds/tags/%s.atom.xml"
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
DISPLAY_CATEGORIES_ON_MENU = False
RELATIVE_URLS = True
STATIC_PATHS = ['images', 'CNAME']
PATH = 'content'
THEME = "tty-theme"
USE_OPEN_GRAPH = False
GOOGLE_ANALYTICS = GOOGLE_ANALYTICS_CODE ="UA-2675698-3"
GOOGLE_ANALYTICS_DOMAIN = "tty.cl"
GOOGLE_ANALYTICS_DOMAIN_UP = False
GITHUB_USER = "freyes"
BOOTSTRAP_THEME = "slate"
EMAIL = "freyes@tty.cl"

TWITTER_ID = "gnusis"
LINKEDIN_ID = "freyesas"
GITHUB_ID = "freyes"
FLICKR_ID = "freyes"
TWITTER_SHARE = True
MD_EXTENSIONS = ['tables', 'codehilite']
