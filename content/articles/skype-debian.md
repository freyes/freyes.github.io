Title: Skype in GNU/Debian AMD64
Author: Felipe Reyes
Date: 2013-02-18 04:59
Category: Debian
Tags: debian, skype, tips

How to install Skype in Debian amd64

- Check if your system has i386 arch support enabled

```
$ dpkg --print-foreign-architectures
i386
```

- If you don't have i386 support enable it with the following commands:

```
# dpkg --add-architecture i386
# apt-get update
```

- Then install the skype's dependencies with the following command:

```
# apt-get install libqtgui4:i386 \
      libqtwebkit4:i386 \
      libqt4-network:i386 \
      libqtcore4:i386 \
      libxss1:i386 \
      lib32stdc++6 \
      libxv1:i386 \
      libasound2:i386 \
      libqt4-dbus:i386 \
      libssl1.0.0:i386 \
      libasound2-plugins:i386 \
      libqt4-xml \
      libqtcore4 \
      libqtdbus4 \
      qdbus
```

- And then you are ready to install skype

```
# dpkg -i skype-debian_4.1.0.20-1_i386.deb
```
