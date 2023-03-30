Title: Deploying a Python WSGI app with Vagrant and Puppet
Date: 2014-01-22
Author: Felipe Reyes
Tags: python, vagrant, puppet, wsgi


These days the tendency among software companies is to have everything under
version control systems (i.e. [Git](http://git-scm.com/),
[Mercurial](http://mercurial.selenic.com/)), all these is part of two software
development strategies: [continuous integration](http://en.wikipedia.org/wiki/Continuous_integration)
and [continuous delivery](http://en.wikipedia.org/wiki/Continuous_delivery).
To read more about them I recommend you to read ["Continuous Integration: Improving Software Quality and Reducing Risk"](http://www.amazon.com/Continuous-Integration-Improving-Software-Reducing/dp/0321336380/ref=sr_1_1?ie=UTF8&qid=1390443569&sr=8-1&keywords=continuous+integration)
and ["Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation"](http://www.amazon.com/Continuous-Delivery-Deployment-Automation-Addison-Wesley/dp/0321601912/ref=sr_1_3?ie=UTF8&qid=1390443569&sr=8-3&keywords=continuous+integration)

So I took [Vagrant](http://www.vagrantup.com/) to provision the machines that
will run my [example webapp](https://github.com/freyes/flask-hello-world), and
[Puppet](http://puppetlabs.com) will take care of configuring my system.

My recipes are in continuous development, so you should refer to the git
repositories for the latest information about how they work.

* [Vagrant and Puppet recipes](https://github.com/freyes/vagrant-puppet-example)
* [Flask hello world](https://github.com/freyes/flask-hello-world)
