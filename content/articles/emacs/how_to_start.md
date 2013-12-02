Title: How to start with Emacs
Date: 2013-12-03

## Part 0

Before I could really be productive with emacs, I failed a couple of
times, because I knew that emacs were powerful, but the default
configuration shows you a simple text editor that look awful, without
syntax highlight, without anti-alias, a color schema that really
sucks.

In GNU/Linux (to not piss off rms xD)I was never found a really nice
(text) editor, because all the available suck at some point (even
emacs sucks sometime, but suck less than the rest :P), so when I met
zeus lead me in the first steps giving me some elisp tips, I could
start swimming by myself and improving my emacs configuration file,
and even teaching some tips to the mentor :P.

So I will start a series of articles of how to start with emacs,
especially giving the recipes (elisp code) of how to obtain the
desired behavior.

## Part 1

First of all, All my tips related to the underlying Operative System
are using GNU/Linux Debian, so if you are using another distribution
(or even another OS) you will have to look for the appropriate way to
do the task, if you send me how to do it with another OS I will add it
to the entry.

### What is emacs?

Well, emacs doesn't exists, the correct name is GNU Emacs for the
series of post, because there is a lot different flavors of emacs, for
example XEmacs, Aquamacs, and others.

The GNU Emacs website says:

    GNU Emacs is an extensible, customizable text editor—and more. At
    its core is an interpreter for Emacs Lisp, a dialect of the Lisp
    programming language with extensions to support text editing.

What can I do with emacs?

It's a text editor, so write text :P, but also:

- Develop software in a wide range of compute languages, like C, C++,
  elisp, C#, ruby, python, java, ...
- Mail client

- Chat with your irc folks

- Surf on the web

- And other things that will be discussed in their respectives posts

### Install GNU Emacs

First you must decide witch version of emacs do you want to use?,
exists emacs22, which is the current stable release, and also emacs23
(aka emacs-cvs) which is the development version, but currently is in
the state of features freeze, so It's pretty stable to me, if you use
emacs22 you will not have anti-alias, something that is very nice to
the eyes when you spend the day developing, almost all the tips
discussed in the series will be neutral, except the related with
anti-alias and multi-tty.

### Debian

To use emacs22 you can just use the debian official archive and
execute

```
apt-get install emacs22
```

But if you want to use the emacs cvs there is a repository maintained
by Romain Francoise of the package emacs-snapshot which is a binary
package of the cvs code (this is the one that I use). To use this repo
you must the following to you source.list (to obtain more details
visit the webpage of the repo)

```
deb http://emacs.naquadah.org/ unstable/
```

Then just install the emacs-snapshot package.

## Part 2

Emacs uses a configuration file that is by default placed in your home
directory, the file is called .emacs (I don't know if on win32 systems
is also called .emacs). This file contents is elisp code, so for full
control of emacs it's imperative learn elisp, but I still didn't learn
elisp and I'm an emacs user :), so you can learn elisp while you are
looking for snippets of code.

### Concepts

I will have to explain some concepts that are important to understand
why emacs behave in the way that it does.

In emacs there are buffers, there is the minibuffer that is where you
type the emacs commands (or elisp interactive functions), and the
other buffers could represent an opened file, a pipe, or just a
temporary editing space that is not attached to a file, the name of
the last type of buffers start and end with *, for example *scratch*

Emacs has something called 'modes', it's something like the way that a
determined buffer must behave, for example if you are going to open C
source code file the c-mode should be loaded, and it will help you in
task of develop with the C language. There are 2 kinds of modes, the
major and minor modes, one buffer can only have one major mode and
zero or more minor modes.

### First tweaks

Emacs is a software with a huge history and tradition, so there are
some things that for somebody that is formed in the last 10 years in
computing terms there some musts that you must have in you emacs
config file, like the transient-mark-mode

The transient mark mode highlights the selected region of text, by
defaults this is disabled so I recommend you enable it with pasting
the following in your .emacs

```
(transient-mark-mode 1)
```

Fill you name and email to let the modes that need that information
could use, this is done with the following snippet of code

```
(setq user-mail-address "homer@example.com")
(setq user-full-name "Homer J. Simpsons")
```

If you like to use Ctrl+g to jump to a line number then you should add
the following code

```
(global-set-key [(control g)] 'goto-line)
```

One of the sweetest feature that must have a text editor is syntax
highlight, well emacs has this, but disabled by default, with the
following code you will have it enabled always

```
(require 'font-lock)
(global-font-lock-mode t)
```

I think that this is enough for this entry, the next entries probably
will be more fun to write and read, because i will start talking about
the major modes, one mode per entry, probably the next one will be the
C mode.

## Emacswiki

  [Emacswiki](http://www.emacswiki.org/) is probably the best source to find emacs-specific tip-n-tricks

## Initial Configuration

Suggested initial configuration:

```elisp
;; to debug the .emacs file
(setq debug-on-error nil)
(setq visible-bell nil)

;; setup the default mode to use
;;Text mode is happier than Fundamental mode ;-)
(setq default-major-mode 'text-mode)

;; define the mail and name
(setq user-mail-address "foo@example.com")
(setq user-full-name "Foo Bar")

;; be nice with X clipboard
(setq x-select-enable-clipboard t)

;; use Control+g fot goto-line
(global-set-key [(control g)] 'goto-line)

;; enable menubar and tool bar
(menu-bar-mode 1)
(tool-bar-mode 1)

;; turn on font-lock mode
(global-font-lock-mode t)
(require 'font-lock) ; enable syntax highlighting

;; simple cut, copy, paste
(global-set-key [f2] 'clipboard-kill-region)
(global-set-key [f3] 'clipboard-kill-ring-save)
(global-set-key [f4] 'clipboard-yank)

(global-set-key [end] 'end-of-line)
(global-set-key [home] 'beginning-of-line)

;;touche del et suppr
(global-set-key [delete] 'delete-char)

;;(dysplay question in 'y/n' instead of 'yes/no')
(fset 'yes-or-no-p 'y-or-n-p)

;; tramp let you open remote files over ssh
(require 'tramp)
(setq tramp-default-method "ssh")

;;; Prevent Extraneous Tabs
(setq-default indent-tabs-mode nil)
```
