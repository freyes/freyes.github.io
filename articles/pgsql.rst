Postgresql Tips n' Tricks
#########################

:author: Felipe Reyes
:date: 2013-11-22 15:23
:tags: postgresql, tips
:category: Postgresql

* pg_stat_activity

`pg_stat_activity <http://www.postgresql.org/docs/current/static/monitoring-stats.html>`_ 
is a view that belongs to the postgresql catalog, it helps you to view the 
status of the queries that are in execution, the explanation of each column
can be found in the postgresql manual `The Statistics Collector <http://www.postgresql.org/docs/current/static/monitoring-stats.html>`_
section (I don't want to do a simply copy-paste, so see the official documentation).

+----------------+--------------------------+-----------+
| Column         | Type                     | Modifiers |
+================+==========================+===========+
| datid          | oid                      |           |
+----------------+--------------------------+-----------+
| datname        | name                     |           |
+----------------+--------------------------+-----------+
| procpid        | integer                  |           |
+----------------+--------------------------+-----------+
| usesysid       | oid                      |           |
+----------------+--------------------------+-----------+
| usename        | name                     |           |
+----------------+--------------------------+-----------+
| current_query  | text                     |           |
+----------------+--------------------------+-----------+
| waiting        | boolean                  |           |
+----------------+--------------------------+-----------+
| xact\_start    | timestamp with time zone |           |
+----------------+--------------------------+-----------+
| query\_start   | timestamp with time zone |           |
+----------------+--------------------------+-----------+
| backend\_start | timestamp with time zone |           |
+----------------+--------------------------+-----------+
| client\_addr   | inet                     |           |
+----------------+--------------------------+-----------+
| client\_port   | integer                  |           |
+----------------+--------------------------+-----------+

.. code-block:: sql

    SELECT * FROM pg_stat_activity;


- If you want to view the queries that are stuck (usually due to a lock or simply waiting for I/O) you can execute the following query:

  .. code-block:: sql

      SELECT * FROM pg_stat_activity WHERE waiting = TRUE;
