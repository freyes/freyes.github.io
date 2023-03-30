Title: Mercurial
Category: vcs
Author: Felipe Reyes
Tags: mercurial, vcs
Date: 2012-12-03 17:42:08

This is my mercurial configuration (~/.hgrc)

    :::
    [ui]
    username = Foo Bar <foobar@example.com>
    merge = emacs
    
    [extensions]
    pager =
    rebase = 
    churn =
    hgshelve = ~/.hg.d/hgshelve.py
    keyword =
    fetch =
    activity=~/.hg.d/hgactivity/activity.py
    mq =
    hg_histedit=~/.hg.d/hg_histedit.py
    color =
    
    [diff]
    git = on
    
    [pager]
    pager = LESS='FSRX' less
    attend = glog
    
    [keywordmaps]
    Author = {author|user}
    Date = {date|utcdate}
    Header = {file},v {node|short} {date|utcdate} {author|user}
    Id = {file|basename},v {node|short} {date|utcdate} {author|user}
    RCSFile = {file|basename},v
    RCSfile = {file|basename},v
    Revision = {node|short}
    Source = {root}/{file},v
    
    [web]
    cacerts = /etc/ssl/certs/ca-certificates.crt
    
    [alias]
    sst = !hg status $($HG root) $HG_ARGS
    
    [merge-tools]
    emacs.args = -q --eval "(ediff-merge-with-ancestor \"$local\" \"$other\" \"$base\" nil \"$output\")"
