Title: erc
date: 2013-12-02

This is my configuration for erc

- erc-cmd-NP function send the current track being played to the current chat buffer (channel or private)
- The connect-* functions provide a quick access to the defined IRC server.

```elisp
;;
;; erc.el
;; Login : <freyes@wampa>
;; Started on  Mon Aug 30 23:04:16 2010 Felipe Reyes
;; $Id$
;; 
(defun erc-cmd-NP (&rest ignore)
  "Display the current EMMS track to the current ERC buffer."
  (let ((string (emms-show)))
    (if string
        (erc-send-message string)
      (message "Nothing is playing!"))))
(defun connect-freenode ()
  (interactive)
  (erc
   :server "irc.freenode.net"
   :port 6667
   :nick "freyes"
   :password "XXXXXX"
   :full-name "Felipe Reyes"))

(defun connect-gnome ()
  (interactive)
  (erc
   :server "irc.gnome.org"
   :port 6667
   :nick "freyes"
   :password "XXXXX"
   :full-name "Felipe Reyes"))

(defun connect-oftc ()
  (interactive)
  (erc
   :server "irc.oftc.net"
   :port 6667
   :nick "freyes"
   :password "XXXXXX"
   :full-name "Felipe Reyes"))

(setq erc-auto-query 'frame)
```
