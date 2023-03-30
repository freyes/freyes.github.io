Title: Lynx: accept cookies always
Date: 2016-08-14

From time to time I need to use [lynx](https://packages.ubuntu.com/lynx) (or
any other text based browser like [links](https://packages.ubuntu.com/links)),
for some reason my fingers usually type `lynx`, but having to accept cookies
every time a new domain tries to send it to me it's annoying, so here is how
you configure it to always accept them.

Add this to your `~/.bashrc` file:

    LYNX_CFG=~/.lynx.cfg
    export LYNX_CFG

Then in `~/.lynx.cfg`:

    INCLUDE:/etc/lynx-cur/lynx.cfg
    FORCE_SSL_COOKIES_SECURE:TRUE
    SET_COOKIES:TRUE
    ACCEPT_ALL_COOKIES:TRUE

And voila!
