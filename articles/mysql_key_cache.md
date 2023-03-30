Title: MySQL and the Key Cache Buffer
Date: 2011-12-18
Author: Jonathan Gonzalez
Tags: mysql, tuning, database, cache

# Why did I learn?

It's always important to recognize why this happened, well, here in my
work a few weeks ago I set up a [few new templates](http://code.google.com/p/mysql-cacti-templates/) for our [Cacti](http://www.cacti.net/), among
many useful templates it comes with some very handy templates for
[MySQL](http://www.mysql.com), it comes with a pretty useful template called 'MyISAM Key Cache'
and we noticed that it was full!! so my boss ask me to figure out and
read about this topic and many others that aren't the main topic
of this article

# Find out your current configuration

Since you may not have cacti installed you may need to know what do
you have and how it's working now.

First the value of your 'key buffer size':

```sql
show variables like 'key%';
```

This will show at least, two good things that may be useful for you,
'key buffer size', yes the size of our key buffer! and
'key cache block size' useful to end our tiny article

Well, now we have to know how the key buffer its used:

```sql
show status like 'Key%';
```

All the rows returned from this command are useful! I'll use and
example of one of our servers:

```
mysql> show status like 'Key%';
+------------------------+-----------+
| Variable_name          | Value     |
+------------------------+-----------+
| Key_blocks_not_flushed | 0         |
| Key_blocks_unused      | 240934    |
| Key_blocks_used        | 97093     |
| Key_read_requests      | 211305615 |
| Key_reads              | 321341    |
| Key_write_requests     | 9268658   |
| Key_writes             | 397761    |
+------------------------+-----------+
7 rows in set (0.00 sec)
```

We now have all the data we need to evaluate  our current situation.

# Use the collected data

We will suppose that the value of 'key buffer size' it's '402653184'
the first things we need to know it's that this value it's in bytes so
if you prefer to manage it in megabytes you need to do the
transformation:

``(402653184/1024)/1024 = 384``

We have a Key cache buffer of 384MB which looks like a lot of space,
but how much of that space it's currently used? well, you will have to
do simple calculation:

```
key_buffer_usage = ( Key_blocks_unused * key_cache_block_size ) / key_buffer_size ) * 100
```

So with our collected that we will suppose that the value of
'key cache block size' it's 1024 which it's the default value.

```
( (240934 * 1024) / 402653184 ) * 100 = 61.2
```

So, we have about 61.2 percent of our buffer used, ok this seems to be
right, but there's another data we may find useful! look this extract
from the [MySQL Documentation](http://dev.mysql.com/doc/):

"The Key reads/Key read requests ratio should normally be less than
0.01."

Ok, what the heck this guys mean by that? Well, let's try our maths to
calculate our ratio!

```
key_reads_ratio =  ( Key_reads / Key_read_requests ) * 100
```

And with our data it will be something like:

``( 321341 / 211305615 ) * 100 = 0.152074046``

So, we have a ratio of about 0.15, this doesn't seem a lot to me, but
according to the documentation it's a lot, well, according to the
maths with less key_reads(keys passed to the 'key buffer') and lots of
'key read requests' our 'key reads ratio' should be lower.

# Test and not necessarily a fix!

OK, so you may want to take a look inside your my.cnf, but come on you
can't restart your database right?

Well, if you access your database as 'root' user you can start to
throw a few commands to set these values!

Let's say we want to set up our key buffer, we should do this:

```sql
set global key_buffer_size=512*1024*1024;
```

Thus, we will set our key_buffer to 512M and our system will have a
lot of more key cached and our ratio will go down! awesome right? but
wait, there's a tricks an some cautions you may want to take!

First, if your database it's on production, when you set the value
your cached keys will be lost, thus, the load of your system will
increase significantly so, do this carefully!

Second, you have to wait a lot to calculate, at first, your
key_reads_ratio will not reflect your situation so wait a bit, well,
if you have a lot of users for your database and queries obviously you
will have to wait less.

# Other Stuffs? no, just the end

Well, I'll still working with some [MySQL](http://www.mysql.com]) optimization things, so, I'll
probably upload more things related to this kind of optimizations.

Remember, creating graphs of your system will always help you to
diagnostic your system =)
