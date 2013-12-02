Title: rxvt-unicode
Date: 2011-06-11 23:10
Category: Tools
Author: Felipe Reyes
Tags: debian, linux, tips, rxvt

The Rxvt terminal is a really good terminal emulator, actually it has been my
default terminal since at least 4 years ago. I started using it after getting
 tired of gnome-terminal (it's too fat and heavy for me).

![Screenshot]({filename}/images/urxvt_shot.20110601.jpg)

To install it you just must do the follow:

```
aptitude install rxvt-unicode
```

If you want to use it as your default x-terminal-emulator you have to
set the proper alternative like this

```
update-alternatives --set x-terminal-emulator /usr/bin/urxvt
```

The configuration must go on your ~/.Xdefaults file, here is my configuration

```
URxvt.foreground: grey90
URxvt.cursorColor: #729fcf
URxvt.font: -xos4-terminus-medium-r-normal--14-140-72-72-c-80-iso8859-15
URxvt.scrollBar: False
URxvt.shading: 50
URxvt.transparent: True
URxvt.fade: 80
URxvt.fadeColor: #e9b96e
URxvt.tintColor: #5c5c5c
URxvt*urgentOnBell: true
URxvt*urllauncher: iceweasel
URxvt*matcher.button:        3
URxvt*depth: 24
URxvt*background: rgba:0000/0000/0000/dddd
```

Once you put the configuration you can reload it using this

```shell
xrdb -merge ~/.Xdefaults
```

Remember to install the terminus fonts if you want to use my configuration

```shell
aptitude install xfonts-terminus xfonts-terminus-dos xfonts-terminus-oblique
```
