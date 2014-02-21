Title: Deploy a Python WSGI app with a Celery worker in Heroku
Date: 2014-02-19
Tags: development
Keywords: heroku, celery, python, wsgi

This article explains how to deploy a WSGI python web app + a
[celery](http://www.celeryproject.org) worker.

A recommended reading before moving forward with Heroku is
[The Process Model](https://devcenter.heroku.com/articles/process-model).

# The Application

The application that we are going to deploy to heroku has the following components:

* WSGI App, it can be a [Django](https://www.djangoproject.com/) or
  [Flask](http://flask.pocoo.org/) application, the important part is that you
  provide a WSGI app as entry point.
* Celery, we will be using a Celery worker to run background tasks, for
  example image resizing.
* Database, well ... you know, we usually want to save data permanently.
* RabbitMQ as message broker.

# The ``Procfile``!

``Procfile`` let the developer declare the commands each dyno has to run,
there are several process' types:

Process Type                                                                          |  Command Example                                          
------------------------------------------------------------------------------------- | -------------------------------------------------------
web                                                                                   |  gunicorn app.wsgi -b 0.0.0.0:$PORT --debug               
worker                                                                                |  celery -A tasks worker --loglevel=info --concurrency=1
[clock](https://devcenter.heroku.com/articles/scheduled-jobs-custom-clock-processes)  |  python foo.py

This file is the key part to instruct Heroku what to run, for the WSGI app
we'll use a ``web`` process and to run the celery worker daemon we use a
``worker`` process. Each of these processes will scale independently according
to your configuration (see
[Scaling Your Dyno Formation](https://devcenter.heroku.com/articles/scaling)).

For our application we are going to use the following ``Procfile``:

<pre>
web: gunicorn app.wsgi -b 0.0.0.0:$PORT --debug
worker: celery -A app.tasks worker --loglevel=info --concurrency=1
</pre>

## Testing your ``Procfile``

One of the nice things about the ``Procfile`` is that can be interpreted by
[Foreman](http://theforeman.org/), so you can test your configuration running
the following command:

<pre>
$ foreman start
17:43:11 web.1    | started with pid 31923
17:43:11 worker.1 | started with pid 31926
17:43:12 web.1    | 2014-02-19 17:43:12 [31925] [INFO] Starting gunicorn 18.0
17:43:12 web.1    | 2014-02-19 17:43:12 [31925] [INFO] Listening at: http://0.0.0.0:5000 (31925)
17:43:12 web.1    | 2014-02-19 17:43:12 [31925] [INFO] Using worker: sync
17:43:12 web.1    | 2014-02-19 17:43:12 [31938] [INFO] Booting worker with pid: 31938
17:43:14 worker.1 | [2014-02-19 17:43:14,119: WARNING/MainProcess] /home/freyes/.virtualenvs/django-todo/local/lib/python2.7/site-packages/celery/apps/worker.py:161: CDeprecationWarning: 
17:43:14 worker.1 | Starting from version 3.2 Celery will refuse to accept pickle by default.
17:43:14 worker.1 | 
17:43:14 worker.1 | The pickle serializer is a security concern as it may give attackers
17:43:14 worker.1 | the ability to execute any command.  It's important to secure
17:43:14 worker.1 | your broker from unauthorized access when using pickle, so we think
17:43:14 worker.1 | that enabling pickle should require a deliberate action and not be
17:43:14 worker.1 | the default choice.
17:43:14 worker.1 | 
17:43:14 worker.1 | If you depend on pickle then you should set a setting to disable this
17:43:14 worker.1 | warning and to be sure that everything will continue working
17:43:14 worker.1 | when you upgrade to Celery 3.2::
17:43:14 worker.1 | 
17:43:14 worker.1 |     CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
17:43:14 worker.1 | 
17:43:14 worker.1 | You must only enable the serializers that you will actually use.
17:43:14 worker.1 | 
17:43:14 worker.1 | 
17:43:14 worker.1 |   warnings.warn(CDeprecationWarning(W_PICKLE_DEPRECATED))
17:43:15 web.1    | 2014-02-19 17:43:15 [31925] [INFO] Handling signal: winch
17:43:15 web.1    | 2014-02-19 17:43:15 [31925] [INFO] SIGWINCH ignored. Not daemonized
17:43:16 worker.1 | [2014-02-19 17:43:16,683: INFO/MainProcess] Connected to amqp://guest@127.0.0.1:5672//
17:43:17 worker.1 | [2014-02-19 17:43:17,323: INFO/MainProcess] mingle: searching for neighbors
17:43:19 worker.1 | [2014-02-19 17:43:19,151: INFO/MainProcess] mingle: all alone
17:43:19 worker.1 | [2014-02-19 17:43:19,750: WARNING/MainProcess] celery@tiefighter ready.
</pre>

If ``foreman start`` works, then your ``Procfile`` is OK.


# Create the app

Once you have configured the ``Profile`` we'll create an application in Heroku
(remember to install [heroku-toolbelt](https://toolbelt.heroku.com/)) running
``heroku create``.

Example output:

<pre>
$ heroku create
Creating murmuring-ravine-4093... done, stack is cedar
http://murmuring-ravine-4093.herokuapp.com/ | git@heroku.com:murmuring-ravine-4093.git
</pre>

This command creates a new heroku app and it adds a new remote to push your code.

``.git/config`` example:

<pre>
[remote "heroku"]
	url = git@heroku.com:desolate-fortress-2758.git
	fetch = +refs/heads/*:refs/remotes/heroku/*
</pre>
    
# Adding a Database

Heroku provides databases via addons, there are several providers, but for
this article we are going to use
[heroku-postgres](https://addons.heroku.com/heroku-postgresql).

To add it to the recently created application run ``heroku addons:add
heroku-postgresql``. Here is an example output:

<pre>
$ heroku addons:add heroku-postgresql
Adding heroku-postgresql on murmuring-ravine-4093... done, v3 (free)
Attached as HEROKU_POSTGRESQL_YELLOW_URL
Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pgbackups:restore.
Use `heroku addons:docs heroku-postgresql` to view documentation.
</pre>

# Adding RabbitMQ

We are using RabbitMQ as message broker for Celery, for this I choose to use
[CloudAMQP](https://addons.heroku.com/cloudamqp), to add it to your app run
``heroku addons:add cloudamqp``. Here is an example output:

<pre>
$ heroku addons:add cloudamqp
Adding cloudamqp on murmuring-ravine-4093... done, v4 (free)
Use `heroku addons:docs cloudamqp` to view documentation.
</pre>

# Adjusting Settings

Heroku passes to your app environment variables with the configuration, this a common practice in the PaaS ecosystem, so you need to modify your app to read config values from it.

Here are examples to setup Celery and Django:

    :::python
    import os
    import dj_database_url

    DEFAULT_AMQP = "amqp://guest:guest@localhost//"
    DEFAULT_DB = "postgres://localhost"
    db_url = os.environ.get("DATABASE_URL", DEFAULT_DB)

    # Django settings
    DATABASES = {"default": dj_database_url.config(default=DEFAULT_DB)}

    # Celery app configuration
    app = Celery("tasks", backend=db_url.replace("postgres://", "db+postgresql://"),
                 broker=os.environ.get("CLOUDAMQP_URL", DEFAULT_AMQP))
    app.BROKER_POOL_LIMIT = 1


# Launch the app!

Now we have everything configured, it's time to launch push our code and let Heroku do the magic running ``git push heroku master``.

<pre>
$ git push heroku master 
Initializing repository, done.
Counting objects: 365, done.
Delta compression using up to 2 threads.
Compressing objects: 100% (148/148), done.
Writing objects: 100% (365/365), 39.08 KiB | 0 bytes/s, done.
Total 365 (delta 206), reused 319 (delta 185)

-----> Python app detected
-----> No runtime.txt provided; assuming python-2.7.6.
-----> Preparing Python runtime (python-2.7.6)
-----> Installing Setuptools (2.1)
-----> Installing Pip (1.5.2)
-----> Installing dependencies using Pip (1.5.2)
       Downloading/unpacking Django==1.5.5 (from -r requirements.txt (line 1))
         Running setup.py (path:/tmp/pip_build_u26118/Django/setup.py) egg_info for package Django
           
       Downloading/unpacking dj-database-url==0.2.1 (from -r requirements.txt (line 2))
         Downloading dj-database-url-0.2.1.tar.gz
         Running setup.py (path:/tmp/pip_build_u26118/dj-database-url/setup.py) egg_info for package dj-database-url
           
       Downloading/unpacking django-extensions==0.9 (from -r requirements.txt (line 3))
         Running setup.py (path:/tmp/pip_build_u26118/django-extensions/setup.py) egg_info for package django-extensions
           
       Downloading/unpacking django-respite==1.2.0 (from -r requirements.txt (line 4))
         Downloading django-respite-1.2.0.tar.gz
         Running setup.py (path:/tmp/pip_build_u26118/django-respite/setup.py) egg_info for package django-respite
           
           warning: no files found matching 'DEPENDENCIES'
       Downloading/unpacking django-widget-tweaks==1.1.2 (from -r requirements.txt (line 5))
         Downloading django-widget-tweaks-1.1.2.tar.gz
         Running setup.py (path:/tmp/pip_build_u26118/django-widget-tweaks/setup.py) egg_info for package django-widget-tweaks
           
       Downloading/unpacking gunicorn==18.0 (from -r requirements.txt (line 6))
         Running setup.py (path:/tmp/pip_build_u26118/gunicorn/setup.py) egg_info for package gunicorn
           
       Downloading/unpacking ipdb==0.7 (from -r requirements.txt (line 7))
         Downloading ipdb-0.7.tar.gz
         Running setup.py (path:/tmp/pip_build_u26118/ipdb/setup.py) egg_info for package ipdb
           
       Downloading/unpacking ipython==1.2.0 (from -r requirements.txt (line 8))
         Running setup.py (path:/tmp/pip_build_u26118/ipython/setup.py) egg_info for package ipython
           
       Downloading/unpacking psycopg2==2.4.5 (from -r requirements.txt (line 9))
         Running setup.py (path:/tmp/pip_build_u26118/psycopg2/setup.py) egg_info for package psycopg2
           
           no previously-included directories found matching 'doc/src/_build'
       Downloading/unpacking readline==6.2.4.1 (from -r requirements.txt (line 10))
         Running setup.py (path:/tmp/pip_build_u26118/readline/setup.py) egg_info for package readline
           
       Downloading/unpacking dj-static (from -r requirements.txt (line 12))
         Downloading dj-static-0.0.5.tar.gz
         Running setup.py (path:/tmp/pip_build_u26118/dj-static/setup.py) egg_info for package dj-static
           
       Downloading/unpacking static (from -r requirements.txt (line 13))
         Downloading static-1.0.2.tar.gz
         Running setup.py (path:/tmp/pip_build_u26118/static/setup.py) egg_info for package static
           
       Downloading/unpacking Celery==3.1.9 (from -r requirements.txt (line 14))
       Downloading/unpacking SQLAlchemy (from -r requirements.txt (line 15))
       Downloading/unpacking pystache (from static->-r requirements.txt (line 13))
         Running setup.py (path:/tmp/pip_build_u26118/pystache/setup.py) egg_info for package pystache
           pystache: using: version '2.1' of <module 'setuptools' from '/app/.heroku/python/lib/python2.7/site-packages/setuptools-2.1-py2.7.egg/setuptools/__init__.pyc'>
           
       Downloading/unpacking kombu>=3.0.12,<4.0 (from Celery==3.1.9->-r requirements.txt (line 14))
       Downloading/unpacking pytz>dev (from Celery==3.1.9->-r requirements.txt (line 14))
         Running setup.py (path:/tmp/pip_build_u26118/pytz/setup.py) egg_info for package pytz
           
           warning: no files found matching '*.pot' under directory 'pytz'
       Downloading/unpacking billiard>=3.3.0.14,<3.4 (from Celery==3.1.9->-r requirements.txt (line 14))
         Running setup.py (path:/tmp/pip_build_u26118/billiard/setup.py) egg_info for package billiard
           
           warning: no files found matching '*.py' under directory 'Lib'
       Downloading/unpacking amqp>=1.4.2,<2.0 (from kombu>=3.0.12,<4.0->Celery==3.1.9->-r requirements.txt (line 14))
       Downloading/unpacking anyjson>=0.3.3 (from kombu>=3.0.12,<4.0->Celery==3.1.9->-r requirements.txt (line 14))
         Downloading anyjson-0.3.3.tar.gz
         Running setup.py (path:/tmp/pip_build_u26118/anyjson/setup.py) egg_info for package anyjson
           
       Installing collected packages: Django, dj-database-url, django-extensions, django-respite, django-widget-tweaks, gunicorn, ipdb, ipython, psycopg2, readline, dj-static, static, Celery, SQLAlchemy, pystache, kombu, pytz, billiard, amqp, anyjson
         Running setup.py install for Django

           changing mode of build/scripts-2.7/django-admin.py from 600 to 755
           
           changing mode of /app/.heroku/python/bin/django-admin.py to 755
         Running setup.py install for dj-database-url
           
         Running setup.py install for django-extensions
           
         Running setup.py install for django-respite
           
           warning: no files found matching 'DEPENDENCIES'
         Running setup.py install for django-widget-tweaks
           
         Running setup.py install for gunicorn
           
           Installing gunicorn_paster script to /app/.heroku/python/bin
           Installing gunicorn script to /app/.heroku/python/bin
           Installing gunicorn_django script to /app/.heroku/python/bin
         Running setup.py install for ipdb
           
           Installing ipdb script to /app/.heroku/python/bin
         Running setup.py install for ipython
           
           Installing ipcontroller script to /app/.heroku/python/bin
           Installing iptest script to /app/.heroku/python/bin
           Installing ipcluster script to /app/.heroku/python/bin
           Installing ipython script to /app/.heroku/python/bin
           Installing pycolor script to /app/.heroku/python/bin
           Installing iplogger script to /app/.heroku/python/bin
           Installing irunner script to /app/.heroku/python/bin
           Installing ipengine script to /app/.heroku/python/bin
         Running setup.py install for psycopg2
           building 'psycopg2._psycopg' extension
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/psycopgmodule.c -o build/temp.linux-x86_64-2.7/psycopg/psycopgmodule.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/green.c -o build/temp.linux-x86_64-2.7/psycopg/green.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/pqpath.c -o build/temp.linux-x86_64-2.7/psycopg/pqpath.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/utils.c -o build/temp.linux-x86_64-2.7/psycopg/utils.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/bytes_format.c -o build/temp.linux-x86_64-2.7/psycopg/bytes_format.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/connection_int.c -o build/temp.linux-x86_64-2.7/psycopg/connection_int.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/connection_type.c -o build/temp.linux-x86_64-2.7/psycopg/connection_type.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/cursor_int.c -o build/temp.linux-x86_64-2.7/psycopg/cursor_int.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/cursor_type.c -o build/temp.linux-x86_64-2.7/psycopg/cursor_type.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/lobject_int.c -o build/temp.linux-x86_64-2.7/psycopg/lobject_int.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/lobject_type.c -o build/temp.linux-x86_64-2.7/psycopg/lobject_type.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/notify_type.c -o build/temp.linux-x86_64-2.7/psycopg/notify_type.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/xid_type.c -o build/temp.linux-x86_64-2.7/psycopg/xid_type.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/adapter_asis.c -o build/temp.linux-x86_64-2.7/psycopg/adapter_asis.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/adapter_binary.c -o build/temp.linux-x86_64-2.7/psycopg/adapter_binary.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/adapter_datetime.c -o build/temp.linux-x86_64-2.7/psycopg/adapter_datetime.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/adapter_list.c -o build/temp.linux-x86_64-2.7/psycopg/adapter_list.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/adapter_pboolean.c -o build/temp.linux-x86_64-2.7/psycopg/adapter_pboolean.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/adapter_pdecimal.c -o build/temp.linux-x86_64-2.7/psycopg/adapter_pdecimal.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/adapter_pint.c -o build/temp.linux-x86_64-2.7/psycopg/adapter_pint.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/adapter_pfloat.c -o build/temp.linux-x86_64-2.7/psycopg/adapter_pfloat.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/adapter_qstring.c -o build/temp.linux-x86_64-2.7/psycopg/adapter_qstring.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/microprotocols.c -o build/temp.linux-x86_64-2.7/psycopg/microprotocols.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/microprotocols_proto.c -o build/temp.linux-x86_64-2.7/psycopg/microprotocols_proto.o -Wdeclaration-after-statement
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DPSYCOPG_DEFAULT_PYDATETIME=1 -DPSYCOPG_VERSION="2.4.5 (dt dec pq3 ext)" -DPG_VERSION_HEX=0x090204 -DPSYCOPG_EXTENSIONS=1 -DPSYCOPG_NEW_BOOLEAN=1 -DHAVE_PQFREEMEM=1 -I/app/.heroku/python/include/python2.7 -I. -I/usr/include/postgresql -I/usr/include/postgresql/9.2/server -c psycopg/typecast.c -o build/temp.linux-x86_64-2.7/psycopg/typecast.o -Wdeclaration-after-statement
           gcc -pthread -shared build/temp.linux-x86_64-2.7/psycopg/psycopgmodule.o build/temp.linux-x86_64-2.7/psycopg/green.o build/temp.linux-x86_64-2.7/psycopg/pqpath.o build/temp.linux-x86_64-2.7/psycopg/utils.o build/temp.linux-x86_64-2.7/psycopg/bytes_format.o build/temp.linux-x86_64-2.7/psycopg/connection_int.o build/temp.linux-x86_64-2.7/psycopg/connection_type.o build/temp.linux-x86_64-2.7/psycopg/cursor_int.o build/temp.linux-x86_64-2.7/psycopg/cursor_type.o build/temp.linux-x86_64-2.7/psycopg/lobject_int.o build/temp.linux-x86_64-2.7/psycopg/lobject_type.o build/temp.linux-x86_64-2.7/psycopg/notify_type.o build/temp.linux-x86_64-2.7/psycopg/xid_type.o build/temp.linux-x86_64-2.7/psycopg/adapter_asis.o build/temp.linux-x86_64-2.7/psycopg/adapter_binary.o build/temp.linux-x86_64-2.7/psycopg/adapter_datetime.o build/temp.linux-x86_64-2.7/psycopg/adapter_list.o build/temp.linux-x86_64-2.7/psycopg/adapter_pboolean.o build/temp.linux-x86_64-2.7/psycopg/adapter_pdecimal.o build/temp.linux-x86_64-2.7/psycopg/adapter_pint.o build/temp.linux-x86_64-2.7/psycopg/adapter_pfloat.o build/temp.linux-x86_64-2.7/psycopg/adapter_qstring.o build/temp.linux-x86_64-2.7/psycopg/microprotocols.o build/temp.linux-x86_64-2.7/psycopg/microprotocols_proto.o build/temp.linux-x86_64-2.7/psycopg/typecast.o -L/usr/lib -lpq -o build/lib.linux-x86_64-2.7/psycopg2/_psycopg.so
           
           no previously-included directories found matching 'doc/src/_build'
         Running setup.py install for readline
           
           ============ Building the readline library ============
           
           readline-6.2/
           readline-6.2/doc/
           readline-6.2/doc/Makefile.in
           readline-6.2/doc/texinfo.tex
           readline-6.2/doc/version.texi
           readline-6.2/doc/fdl.texi
           readline-6.2/doc/rlman.texi
           readline-6.2/doc/rltech.texi
           readline-6.2/doc/rluser.texi
           readline-6.2/doc/rluserman.texi
           readline-6.2/doc/history.texi
           readline-6.2/doc/hstech.texi
           readline-6.2/doc/hsuser.texi
           readline-6.2/doc/readline.3
           readline-6.2/doc/history.3
           readline-6.2/doc/texi2dvi
           readline-6.2/doc/texi2html
           readline-6.2/doc/readline.ps
           readline-6.2/doc/history.ps
           readline-6.2/doc/rluserman.ps
           readline-6.2/doc/readline.dvi
           readline-6.2/doc/history.dvi
           readline-6.2/doc/rluserman.dvi
           readline-6.2/doc/readline.info
           readline-6.2/doc/history.info
           readline-6.2/doc/rluserman.info
           readline-6.2/doc/readline.html
           readline-6.2/doc/history.html
           readline-6.2/doc/rluserman.html
           readline-6.2/doc/readline.0
           readline-6.2/doc/history.0
           readline-6.2/doc/readline_3.ps
           readline-6.2/doc/history_3.ps
           readline-6.2/doc/history.pdf
           readline-6.2/doc/readline.pdf
           readline-6.2/doc/rluserman.pdf
           readline-6.2/examples/
           readline-6.2/examples/autoconf/
           readline-6.2/examples/autoconf/BASH_CHECK_LIB_TERMCAP
           readline-6.2/examples/autoconf/RL_LIB_READLINE_VERSION
           readline-6.2/examples/autoconf/wi_LIB_READLINE
           readline-6.2/examples/rlfe/
           readline-6.2/examples/rlfe/ChangeLog
           readline-6.2/examples/rlfe/Makefile.in
           readline-6.2/examples/rlfe/README
           readline-6.2/examples/rlfe/config.h.in
           readline-6.2/examples/rlfe/configure
           readline-6.2/examples/rlfe/configure.in
           readline-6.2/examples/rlfe/extern.h
           readline-6.2/examples/rlfe/os.h
           readline-6.2/examples/rlfe/pty.c
           readline-6.2/examples/rlfe/rlfe.c
           readline-6.2/examples/rlfe/screen.h
           readline-6.2/examples/Makefile.in
           readline-6.2/examples/excallback.c
           readline-6.2/examples/fileman.c
           readline-6.2/examples/manexamp.c
           readline-6.2/examples/readlinebuf.h
           readline-6.2/examples/rl-fgets.c
           readline-6.2/examples/rlcat.c
           readline-6.2/examples/rlevent.c
           readline-6.2/examples/rltest.c
           readline-6.2/examples/rl.c
           readline-6.2/examples/rlptytest.c
           readline-6.2/examples/rlversion.c
           readline-6.2/examples/histexamp.c
           readline-6.2/examples/Inputrc
           readline-6.2/examples/rlwrap-0.30.tar.gz
           readline-6.2/support/
           readline-6.2/support/config.guess
           readline-6.2/support/config.rpath
           readline-6.2/support/config.sub
           readline-6.2/support/install.sh
           readline-6.2/support/mkdirs
           readline-6.2/support/mkdist
           readline-6.2/support/mkinstalldirs
           readline-6.2/support/shobj-conf
           readline-6.2/support/shlib-install
           readline-6.2/support/wcwidth.c
           readline-6.2/shlib/
           readline-6.2/shlib/Makefile.in
           readline-6.2/COPYING
           readline-6.2/README
           readline-6.2/MANIFEST
           readline-6.2/INSTALL
           readline-6.2/CHANGELOG
           readline-6.2/CHANGES
           readline-6.2/NEWS
           readline-6.2/USAGE
           readline-6.2/aclocal.m4
           readline-6.2/config.h.in
           readline-6.2/configure
           readline-6.2/configure.in
           readline-6.2/Makefile.in
           readline-6.2/ansi_stdlib.h
           readline-6.2/chardefs.h
           readline-6.2/history.h
           readline-6.2/histlib.h
           readline-6.2/keymaps.h
           readline-6.2/posixdir.h
           readline-6.2/posixjmp.h
           readline-6.2/readline.h
           readline-6.2/posixselect.h
           readline-6.2/posixstat.h
           readline-6.2/rlconf.h
           readline-6.2/rldefs.h
           readline-6.2/rlmbutil.h
           readline-6.2/rlprivate.h
           readline-6.2/rlshell.h
           readline-6.2/rlstdc.h
           readline-6.2/rltty.h
           readline-6.2/rltypedefs.h
           readline-6.2/rlwinsize.h
           readline-6.2/tcap.h
           readline-6.2/tilde.h
           readline-6.2/xmalloc.h
           readline-6.2/bind.c
           readline-6.2/callback.c
           readline-6.2/compat.c
           readline-6.2/complete.c
           readline-6.2/display.c
           readline-6.2/emacs_keymap.c
           readline-6.2/funmap.c
           readline-6.2/input.c
           readline-6.2/isearch.c
           readline-6.2/keymaps.c
           readline-6.2/kill.c
           readline-6.2/macro.c
           readline-6.2/mbutil.c
           readline-6.2/misc.c
           readline-6.2/nls.c
           readline-6.2/parens.c
           readline-6.2/readline.c
           readline-6.2/rltty.c
           readline-6.2/savestring.c
           readline-6.2/search.c
           readline-6.2/shell.c
           readline-6.2/signals.c
           readline-6.2/terminal.c
           readline-6.2/text.c
           readline-6.2/tilde.c
           readline-6.2/undo.c
           readline-6.2/util.c
           readline-6.2/vi_keymap.c
           readline-6.2/vi_mode.c
           readline-6.2/xfree.c
           readline-6.2/xmalloc.c
           readline-6.2/history.c
           readline-6.2/histexpand.c
           readline-6.2/histfile.c
           readline-6.2/histsearch.c
           readline-6.2/patchlevel
           patching file vi_mode.c
           patching file callback.c
           patching file support/shobj-conf
           patching file patchlevel
           patching file input.c
           patching file patchlevel
           patching file vi_mode.c
           patching file patchlevel
           checking build system type... x86_64-unknown-linux-gnu
           checking host system type... x86_64-unknown-linux-gnu
           
           Beginning configuration for readline-6.2 for x86_64-unknown-linux-gnu
           
           checking whether make sets $(MAKE)... yes
           checking for gcc... gcc
           checking for C compiler default output file name... a.out
           checking whether the C compiler works... yes
           checking whether we are cross compiling... no
           checking for suffix of executables...
           checking for suffix of object files... o
           checking whether we are using the GNU C compiler... yes
           checking whether gcc accepts -g... yes
           checking for gcc option to accept ISO C89... none needed
           checking how to run the C preprocessor... gcc -E
           checking for grep that handles long lines and -e... /bin/grep
           checking for egrep... /bin/grep -E
           checking for ANSI C header files... yes
           checking for sys/types.h... yes
           checking for sys/stat.h... yes
           checking for stdlib.h... yes
           checking for string.h... yes
           checking for memory.h... yes
           checking for strings.h... yes
           checking for inttypes.h... yes
           checking for stdint.h... yes
           checking for unistd.h... yes
           checking minix/config.h usability... no
           checking minix/config.h presence... no
           checking for minix/config.h... no
           checking whether it is safe to define __EXTENSIONS__... yes
           checking whether gcc needs -traditional... no
           checking for a BSD-compatible install... /usr/bin/install -c
           checking for ar... ar
           checking for ranlib... ranlib
           checking for an ANSI C-conforming const... yes
           checking for function prototypes... yes
           checking whether char is unsigned... no
           checking for working volatile... yes
           checking return type of signal handlers... void
           checking for size_t... yes
           checking for ssize_t... yes
           checking for ANSI C header files... (cached) yes
           checking whether stat file-mode macros are broken... no
           checking for dirent.h that defines DIR... yes
           checking for library containing opendir... none required
           checking for fcntl... yes
           checking for kill... yes
           checking for lstat... yes
           checking for memmove... yes
           checking for putenv... yes
           checking for select... yes
           checking for setenv... yes
           checking for setlocale... yes
           checking for strcasecmp... yes
           checking for strpbrk... yes
           checking for tcgetattr... yes
           checking for vsnprintf... yes
           checking for isascii... yes
           checking for isxdigit... yes
           checking for getpwent... yes
           checking for getpwnam... yes
           checking for getpwuid... yes
           checking for working strcoll... yes
           checking fcntl.h usability... yes
           checking fcntl.h presence... yes
           checking for fcntl.h... yes
           checking for unistd.h... (cached) yes
           checking for stdlib.h... (cached) yes
           checking varargs.h usability... no
           checking varargs.h presence... no
           checking for varargs.h... no
           checking stdarg.h usability... yes
           checking stdarg.h presence... yes
           checking for stdarg.h... yes
           checking for string.h... (cached) yes
           checking for strings.h... (cached) yes
           checking limits.h usability... yes
           checking limits.h presence... yes
           checking for limits.h... yes
           checking locale.h usability... yes
           checking locale.h presence... yes
           checking for locale.h... yes
           checking pwd.h usability... yes
           checking pwd.h presence... yes
           checking for pwd.h... yes
           checking for memory.h... (cached) yes
           checking termcap.h usability... yes
           checking termcap.h presence... yes
           checking for termcap.h... yes
           checking termios.h usability... yes
           checking termios.h presence... yes
           checking for termios.h... yes
           checking termio.h usability... yes
           checking termio.h presence... yes
           checking for termio.h... yes
           checking sys/pte.h usability... no
           checking sys/pte.h presence... no
           checking for sys/pte.h... no
           checking sys/stream.h usability... no
           checking sys/stream.h presence... no
           checking for sys/stream.h... no
           checking sys/select.h usability... yes
           checking sys/select.h presence... yes
           checking for sys/select.h... yes
           checking sys/file.h usability... yes
           checking sys/file.h presence... yes
           checking for sys/file.h... yes
           checking for sys/ptem.h... no
           checking for special C compiler options needed for large files... no
           checking for _FILE_OFFSET_BITS value needed for large files... no
           checking for type of signal functions... posix
           checking if signal handlers must be reinstalled when invoked... no
           checking for presence of POSIX-style sigsetjmp/siglongjmp... present
           checking for lstat... yes
           checking whether or not strcoll and strcmp differ... no
           checking whether the ctype macros accept non-ascii characters... no
           checking whether getpw functions are declared in pwd.h... yes
           checking whether termios.h defines TIOCGWINSZ... no
           checking whether sys/ioctl.h defines TIOCGWINSZ... yes
           checking for sig_atomic_t in signal.h... yes
           checking whether signal handlers are of type void... yes
           checking for TIOCSTAT in sys/ioctl.h... no
           checking for FIONREAD in sys/ioctl.h... yes
           checking for speed_t in sys/types.h... no
           checking for struct winsize in sys/ioctl.h and termios.h... sys/ioctl.h
           checking for struct dirent.d_ino... yes
           checking for struct dirent.d_fileno... yes
           checking for tgetent... no
           checking for tgetent in -ltermcap... yes
           checking which library has the termcap functions... using libtermcap
           checking wctype.h usability... yes
           checking wctype.h presence... yes
           checking for wctype.h... yes
           checking wchar.h usability... yes
           checking wchar.h presence... yes
           checking for wchar.h... yes
           checking langinfo.h usability... yes
           checking langinfo.h presence... yes
           checking for langinfo.h... yes
           checking for mbrlen... yes
           checking for mbscasecmp... no
           checking for mbscmp... no
           checking for mbsnrtowcs... yes
           checking for mbsrtowcs... yes
           checking for mbschr... no
           checking for wcrtomb... yes
           checking for wcscoll... yes
           checking for wcsdup... yes
           checking for wcwidth... yes
           checking for wctype... yes
           checking for wcswidth... yes
           checking whether mbrtowc and mbstate_t are properly declared... yes
           checking for iswlower... yes
           checking for iswupper... yes
           checking for towlower... yes
           checking for towupper... yes
           checking for iswctype... yes
           checking for nl_langinfo and CODESET... yes
           checking for wchar_t in wchar.h... yes
           checking for wctype_t in wctype.h... yes
           checking for wint_t in wctype.h... yes
           checking configuration for building shared libraries... supported
           configure: creating ./config.status
           config.status: creating Makefile
           config.status: creating doc/Makefile
           config.status: creating examples/Makefile
           config.status: creating shlib/Makefile
           config.status: creating config.h
           config.status: executing default commands
           rm -f readline.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O readline.c
           rm -f vi_mode.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O vi_mode.c
           rm -f funmap.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O funmap.c
           rm -f keymaps.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O keymaps.c
           rm -f parens.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O parens.c
           rm -f search.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O search.c
           rm -f rltty.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O rltty.c
           rm -f complete.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O complete.c
           rm -f bind.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O bind.c
           rm -f isearch.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O isearch.c
           rm -f display.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O display.c
           rm -f signals.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O signals.c
           rm -f util.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O util.c
           util.c: In function ‘_rl_tropen’:
           util.c:510: warning: format ‘%ld’ expects type ‘long int’, but argument 3 has type ‘__pid_t’
           rm -f kill.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O kill.c
           rm -f undo.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O undo.c
           rm -f macro.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O macro.c
           rm -f input.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O input.c
           rm -f callback.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O callback.c
           rm -f terminal.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O terminal.c
           rm -f text.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O text.c
           rm -f nls.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O nls.c
           rm -f misc.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O misc.c
           rm -f compat.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O compat.c
           rm -f xfree.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O xfree.c
           rm -f xmalloc.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O xmalloc.c
           rm -f history.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O history.c
           rm -f histexpand.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O histexpand.c
           rm -f histfile.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O histfile.c
           histfile.c: In function ‘history_truncate_file’:
           histfile.c:406: warning: ignoring return value of ‘write’, declared with attribute warn_unused_result
           rm -f histsearch.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O histsearch.c
           rm -f shell.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O shell.c
           rm -f mbutil.o
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O mbutil.c
           rm -f tilde.o
           gcc -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I. -DRL_LIBRARY_VERSION='"6.2"' -g -O -DREADLINE_LIBRARY -c ./tilde.c
           rm -f libreadline.a
           ar cr libreadline.a readline.o vi_mode.o funmap.o keymaps.o parens.o search.o rltty.o complete.o bind.o isearch.o display.o signals.o util.o kill.o undo.o macro.o input.o callback.o terminal.o text.o nls.o misc.o compat.o xfree.o xmalloc.o history.o histexpand.o histfile.o histsearch.o shell.o mbutil.o tilde.o
           test -n "ranlib" && ranlib libreadline.a
           rm -f libhistory.a
           ar cr libhistory.a history.o histexpand.o histfile.o histsearch.o shell.o mbutil.o xmalloc.o xfree.o
           test -n "ranlib" && ranlib libhistory.a
           test -d shlib || mkdir shlib
           ( cd shlib ; make  all )
           make[1]: Entering directory `/tmp/pip_build_u26118/readline/rl/readline-lib/shlib'
           rm -f readline.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o readline.o ../readline.c
           mv readline.o readline.so
           rm -f vi_mode.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o vi_mode.o ../vi_mode.c
           mv vi_mode.o vi_mode.so
           rm -f funmap.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o funmap.o ../funmap.c
           mv funmap.o funmap.so
           rm -f keymaps.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o keymaps.o ../keymaps.c
           mv keymaps.o keymaps.so
           rm -f parens.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o parens.o ../parens.c
           mv parens.o parens.so
           rm -f search.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o search.o ../search.c
           mv search.o search.so
           rm -f rltty.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o rltty.o ../rltty.c
           mv rltty.o rltty.so
           rm -f complete.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o complete.o ../complete.c
           mv complete.o complete.so
           rm -f bind.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o bind.o ../bind.c
           mv bind.o bind.so
           rm -f isearch.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o isearch.o ../isearch.c
           mv isearch.o isearch.so
           rm -f display.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o display.o ../display.c
           mv display.o display.so
           rm -f signals.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o signals.o ../signals.c
           mv signals.o signals.so
           rm -f util.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o util.o ../util.c
           ../util.c: In function ‘_rl_tropen’:
           ../util.c:510: warning: format ‘%ld’ expects type ‘long int’, but argument 3 has type ‘__pid_t’
           mv util.o util.so
           rm -f kill.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o kill.o ../kill.c
           mv kill.o kill.so
           rm -f undo.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o undo.o ../undo.c
           mv undo.o undo.so
           rm -f macro.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o macro.o ../macro.c
           mv macro.o macro.so
           rm -f input.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o input.o ../input.c
           mv input.o input.so
           rm -f callback.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o callback.o ../callback.c
           mv callback.o callback.so
           rm -f terminal.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o terminal.o ../terminal.c
           mv terminal.o terminal.so
           rm -f text.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o text.o ../text.c
           mv text.o text.so
           rm -f nls.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o nls.o ../nls.c
           mv nls.o nls.so
           rm -f misc.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o misc.o ../misc.c
           mv misc.o misc.so
           rm -f xmalloc.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o xmalloc.o ../xmalloc.c
           mv xmalloc.o xmalloc.so
           rm -f xfree.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o xfree.o ../xfree.c
           mv xfree.o xfree.so
           rm -f history.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o history.o ../history.c
           mv history.o history.so
           rm -f histexpand.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o histexpand.o ../histexpand.c
           mv histexpand.o histexpand.so
           rm -f histfile.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o histfile.o ../histfile.c
           ../histfile.c: In function ‘history_truncate_file’:
           ../histfile.c:406: warning: ignoring return value of ‘write’, declared with attribute warn_unused_result
           mv histfile.o histfile.so
           rm -f histsearch.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o histsearch.o ../histsearch.c
           mv histsearch.o histsearch.so
           rm -f shell.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o shell.o ../shell.c
           mv shell.o shell.so
           rm -f mbutil.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o mbutil.o ../mbutil.c
           mv mbutil.o mbutil.so
           rm -f tilde.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -DREADLINE_LIBRARY -c -o tilde.o ../tilde.c
           mv tilde.o tilde.so
           rm -f compat.so
           gcc -c -DHAVE_CONFIG_H   -DNEED_EXTERN_PC -fPIC -I. -I.. -I.. -DRL_LIBRARY_VERSION='"6.2"' -g -O -fPIC -o compat.o ../compat.c
           mv compat.o compat.so
           rm -f libreadline.so.6.2
           gcc -shared -Wl,-soname,libreadline.so.6.2 -Wl,-rpath,/usr/local/lib -Wl,-soname,`basename libreadline.so.6.2 .2` -o libreadline.so.6.2 readline.so vi_mode.so funmap.so keymaps.so parens.so search.so rltty.so complete.so bind.so isearch.so display.so signals.so util.so kill.so undo.so macro.so input.so callback.so terminal.so text.so nls.so misc.so xmalloc.so xfree.so history.so histexpand.so histfile.so histsearch.so shell.so mbutil.so tilde.so compat.so
           rm -f libhistory.so.6.2
           gcc -shared -Wl,-soname,libhistory.so.6.2 -Wl,-rpath,/usr/local/lib -Wl,-soname,`basename libhistory.so.6.2 .2` -o libhistory.so.6.2 history.so histexpand.so histfile.so histsearch.so shell.so mbutil.so xmalloc.so xfree.so
           make[1]: Leaving directory `/tmp/pip_build_u26118/readline/rl/readline-lib/shlib'
           
           ============ Building the readline extension module ============
           
           building 'readline' extension
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DHAVE_RL_CALLBACK -DHAVE_RL_CATCH_SIGNAL -DHAVE_RL_COMPLETION_APPEND_CHARACTER -DHAVE_RL_COMPLETION_DISPLAY_MATCHES_HOOK -DHAVE_RL_COMPLETION_MATCHES -DHAVE_RL_COMPLETION_SUPPRESS_APPEND -DHAVE_RL_PRE_INPUT_HOOK -I. -I/app/.heroku/python/include/python2.7 -c Modules/2.x/readline.c -o build/temp.linux-x86_64-2.7/Modules/2.x/readline.o -Wno-strict-prototypes
           gcc -pthread -shared build/temp.linux-x86_64-2.7/Modules/2.x/readline.o readline/libreadline.a readline/libhistory.a -lncurses -o build/lib.linux-x86_64-2.7/readline.so
           
         Running setup.py install for dj-static
           
         Running setup.py install for static
           
           Installing static script to /app/.heroku/python/bin
         Running setup.py install for pystache
           pystache: using: version '2.1' of <module 'setuptools' from '/app/.heroku/python/lib/python2.7/site-packages/setuptools-2.1-py2.7.egg/setuptools/__init__.pyc'>
           
           Installing pystache script to /app/.heroku/python/bin
           Installing pystache-test script to /app/.heroku/python/bin
         Running setup.py install for pytz
           
           warning: no files found matching '*.pot' under directory 'pytz'
         Running setup.py install for billiard
           building '_billiard' extension
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DHAVE_SEM_OPEN=1 -DHAVE_FD_TRANSFER=1 -DHAVE_SEM_TIMEDWAIT=1 -IModules/_billiard -I/app/.heroku/python/include/python2.7 -c Modules/_billiard/multiprocessing.c -o build/temp.linux-x86_64-2.7/Modules/_billiard/multiprocessing.o
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DHAVE_SEM_OPEN=1 -DHAVE_FD_TRANSFER=1 -DHAVE_SEM_TIMEDWAIT=1 -IModules/_billiard -I/app/.heroku/python/include/python2.7 -c Modules/_billiard/socket_connection.c -o build/temp.linux-x86_64-2.7/Modules/_billiard/socket_connection.o
           gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -DHAVE_SEM_OPEN=1 -DHAVE_FD_TRANSFER=1 -DHAVE_SEM_TIMEDWAIT=1 -IModules/_billiard -I/app/.heroku/python/include/python2.7 -c Modules/_billiard/semaphore.c -o build/temp.linux-x86_64-2.7/Modules/_billiard/semaphore.o
           gcc -pthread -shared build/temp.linux-x86_64-2.7/Modules/_billiard/multiprocessing.o build/temp.linux-x86_64-2.7/Modules/_billiard/socket_connection.o build/temp.linux-x86_64-2.7/Modules/_billiard/semaphore.o -lrt -o build/lib.linux-x86_64-2.7/_billiard.so
           
           warning: no files found matching '*.py' under directory 'Lib'
         Running setup.py install for anyjson
           
       Successfully installed Django dj-database-url django-extensions django-respite django-widget-tweaks gunicorn ipdb ipython psycopg2 readline dj-static static Celery SQLAlchemy pystache kombu pytz billiard amqp anyjson
       Cleaning up...
-----> Collecting static files
       /app/.heroku/python/lib/python2.7/site-packages/django/conf/urls/defaults.py:3: DeprecationWarning: django.conf.urls.defaults is deprecated; use django.conf.urls instead
       0 static files copied.

-----> Discovering process types
       Procfile declares types -> web, worker

-----> Compressing... done, 44.2MB
-----> Launching... done, v6
       http://murmuring-ravine-4093.herokuapp.com deployed to Heroku

To git@heroku.com:murmuring-ravine-4093.git
 * [new branch]      master -> master
</pre>

# Initialize the Database

We have our app running ... but the database wasn't initialized
