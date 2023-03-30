Title: Deploy a Python WSGI app with a Celery worker in Heroku
Date: 2014-02-24
Tags: development
Keywords: heroku, celery, python, wsgi

This article explains how to deploy a WSGI python web app + a
[celery](http://www.celeryproject.org) worker.

A recommended reading before moving forward with Heroku is
[The Process Model](https://devcenter.heroku.com/articles/process-model).

![Jimsy](/images/jimsy.png)

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
[...SNIP...]
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



We have our app running ... but the database wasn't initialized. We are using
Django in this example and we are going to run ``python manage.py syncdb
--noinput``, but for other frameworks you just replace the command with the
one you use to initialize/bootstrap the database.

<pre>
$ heroku run python manage.py syncdb --noinput
Running `python manage.py syncdb --noinput` attached to terminal... up, run.5257
/app/.heroku/python/lib/python2.7/site-packages/django/conf/urls/defaults.py:3: DeprecationWarning: django.conf.urls.defaults is deprecated; use django.conf.urls instead
  DeprecationWarning)

Creating tables ...
Creating table auth_permission
Creating table auth_group_permissions
Creating table auth_group
Creating table auth_user_groups
Creating table auth_user_user_permissions
Creating table auth_user
Creating table django_content_type
Creating table django_session
Creating table django_site
Creating table tasks_task
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)
</pre>

And now we are ready to take a look to our app running ``heroku open`` which will open your browser pointing to your app.

# What now?

We have the app running and a celery worker, now it's moment to assign a
decent domain and other minor settings, heroku provides an option called
[Production Check](https://devcenter.heroku.com/articles/production-check),
you should use it before going live with your site.
