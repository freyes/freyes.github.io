Title: .emacs
Date: 2013-12-02

I hope you enjoy disecting my emacs config :D

```elisp
;; to debug the .emacs file
(setq debug-on-error nil)

;; setup the default mode to use
;;Text mode is happier than Fundamental mode ;-)
(setq default-major-mode 'text-mode)

;; define the mail and name
(setq user-mail-address "your@mail.com")
(setq user-full-name "Your Name")

;;;;;;;;;;;;,;
;; UI setup ;;
;;;;;;;;;;;;;;
(require 'swbuff)
(require 'linum)
;; setup the tab to 4 spaces width
(setq tab-width 4)

(if (eq window-system 'x)
    (set-face-attribute 'default nil :font "Consolas-10"))
;; avoid minimize on C-z, but only in X
(if (eq window-system 'x)
    (global-set-key [C-z] nil))

;; setup default font for mac
(if (eq system-type 'darwin)
    (set-face-attribute 'default nil :font "Consolas-14"))

(tool-bar-mode -1) ;; turn off toolbar
(scroll-bar-mode -1) ;; turn off scrollbar

;; Show tabs
(defface extra-whitespace-face
  '((t (:background "dim gray")))
  "Used for tabs and such.")
(defvar my-extra-keywords
  '(("\t" . 'extra-whitespace-face)))

;; color-theme
(add-to-list 'load-path "~/.emacs.d/elisp/color-theme/")
(require 'color-theme)
;; (require 'color-theme-tango)
;; (color-theme-tango)

(require 'color-theme-arjen)
(color-theme-arjen)

(iswitchb-mode 1)
(global-set-key (kbd "<C-tag>")           'swbuff-switch-to-next-buffer)
(global-set-key (kbd "<C-S-iso-lefttab>") 'swbuff-switch-to-previous-buffer)

;;;;;;;;;;
;; Text ;;
;;;;;;;;;;
(add-hook 'text-mode-hook
          (lambda () (font-lock-add-keywords nil my-extra-keywords)))

;;;;;;;;;;;;;;;
;; rect-mark ;;
;;;;;;;;;;;;;;;
(require 'rect-mark)
(global-set-key (kbd "C-x r C-SPC") 'rm-set-mark)
(global-set-key (kbd "C-x r C-x")   'rm-exchange-point-and-mark)
(global-set-key (kbd "C-x r C-w")   'rm-kill-region)
(global-set-key (kbd "C-x r M-w")   'rm-kill-ring-save)

;;;;;;;;;
;; sql ;;
;;;;;;;;;
(add-hook 'sql-mode-hook
           (lambda ()
             (font-lock-add-keywords nil my-extra-keywords)))

;;;;;;;;;;;;;;
;; Org mode ;;
;;;;;;;;;;;;;;
(load-file "~/.emacs.d/org-mode.el")

;;;;;;;;;;;;;;;;;;;;
;; remember notes ;;
;;;;;;;;;;;;;;;;;;;;
(add-to-list 'load-path "~/.emacs.d/elisp/remember-el")

;; (require 'remember-autoloads)
(autoload 'remember "remember" nil t)
(setq remember-data-file "~/.notes.txt")
(global-set-key (kbd "C-c r") 'remember)

(defun wicked/remember-review-file ()
  "Open `remember-data-file'."
  (interactive)
  (find-file-other-window remember-data-file))
(global-set-key (kbd "C-c r") 'wicked/remember-review-file)

;;;;;;;;;;;;;;;
;; yasnippet ;;
;;;;;;;;;;;;;;;
(require 'yasnippet)
(yas/initialize)
(yas/load-directory "~/.emacs.d/snippets/")

;;;;;;;;;;;;;;;;
;; javascript ;;
;;;;;;;;;;;;;;;;
(autoload 'js2-mode "js2-mode" nil t)
(add-to-list 'auto-mode-alist
             '("\\.js$" . js2-mode))

(add-to-list 'auto-mode-alist
             '("\\.dot$" . graphviz-dot-mode))

;;;;;;;;;;;
;; dired ;;
;;;;;;;;;;;
(require 'dired-x)
(require 'dired-single) ;; http://www.northbound-train.com/emacs/dired-single.el
(defun my-dired-init ()
  "Bunch of stuff to run for dired, either immediately or when it's
         loaded."
  ;; <add other stuff here>
  (define-key dired-mode-map [return] 'dired-single-buffer)
  (define-key dired-mode-map [mouse-1] 'dired-single-buffer-mouse)
  (define-key dired-mode-map "^"
    (function
     (lambda nil (interactive) (dired-single-buffer "..")))))

;; if dired's already loaded, then the keymap will be bound
(if (boundp 'dired-mode-map)
    ;; we're good to go; just add our bindings
    (my-dired-init)
  ;; it's not loaded yet, so add our bindings to the load-hook
  (add-hook 'dired-load-hook 'my-dired-init))

(setq dired-omit-files-p t)
(setq-default dired-omit-files-p t) ; this is buffer-local variable
(setq dired-omit-files
      (concat dired-omit-files "*\.tsv|\\|^\\..+$"))

;;;;;;;;;;
;; yaml ;;
;;;;;;;;;;
(require 'yaml-mode)
(add-to-list 'auto-mode-alist '("\\.yml$" . yaml-mode))
(add-to-list 'auto-mode-alist '("\\.yaml$" . yaml-mode))

;;;;;;;;;;;;;;;;
;; multi-term ;;
;;;;;;;;;;;;;;;;
(autoload 'multi-term "multi-term" nil t)
(autoload 'multi-term-next "multi-term" nil t)

(setq multi-term-program "/bin/bash")   ;; use bash
;; (setq multi-term-program "/bin/zsh") ;; or use zsh...

;; only needed if you use autopair
;; (add-hook 'term-mode-hook
;;   #'(lambda () (setq autopair-dont-activate t)))

(global-set-key (kbd "C-c t") 'multi-term-next)
(global-set-key (kbd "C-c T") 'multi-term) ;; create a new one

;; use Control+g fot goto-line
(global-set-key [(control g)] 'goto-line)

;;;;;;;;;;;;
;; Python ;;
;;;;;;;;;;;;

(setq py-python-command "/usr/bin/python")

(setq auto-mode-alist (cons '("\\.py$" . python-mode) auto-mode-alist))
(setq interpreter-mode-alist (cons '("python" . python-mode)
                                   interpreter-mode-alist))
(autoload 'python-mode "python-mode" "Python editing mode." t)

;; show pydoc
;; http://www.emacswiki.org/cgi-bin/wiki/PythonMode
(defun my-python-documentation (w)
  "Launch PyDOC on the Word at Point"
  (interactive
   (list (let* ((word (thing-at-point 'word))
                (input (read-string
                        (format "pydoc entry%s: "
                                (if (not word) "" (format " (default %s)" word))))))
           (if (string= input "")
               (if (not word) (error "No pydoc args given")
                 word) ;sinon word
             input)))) ;sinon input
  (shell-command (concat py-python-command " -c \"from pydoc import help;help(\'" w "\')\"") "*PYDOCS*")
  (view-buffer-other-window "*PYDOCS*" t 'kill-buffer-and-window))

;;to show the pydoc help on the word at point
(add-hook 'python-mode-hook
          (function (lambda ()
                      (local-set-key [(control f1)] 'my-python-documentation)
                      )))

;;para indentar o completar con tab
(add-hook 'python-mode-hook
          (function (lambda ()
                      (local-set-key (kbd "<tab>") 'indent-or-complete)
                      )))
(add-hook 'python-mode-hook
          (function (lambda ()
                      (local-set-key (kbd "C-x #") 'comment-or-uncomment-region)
                      )))

;;pdb setup, note the python version
(setq pdb-path '/usr/bin/pdb
      gud-pdb-command-name (symbol-name pdb-path))
(defadvice pdb (before gud-query-cmdline activate)
  "Provide a better default command line when called interactively."
  (interactive
   (list (gud-query-cmdline pdb-path
                            (file-name-nondirectory buffer-file-name)))))

;; para usar pdb con F8
(add-hook 'python-mode-hook
          (function (lambda ()
                      (local-set-key (kbd "<f8>") 'pdb)
                      )))
;; para usar pydoc
(add-hook 'python-mode-hook
          '(lambda () (eldoc-mode 1)) t)

;;show tab in python mode
(add-hook 'python-mode-hook
          (lambda ()
            (font-lock-add-keywords nil my-extra-keywords)))

;; para mostrar el trailing whitespace
(add-hook 'python-mode-hook
          (lambda ()
            (setq show-trailing-whitespace t)))

;; usar pylint
(when (load "flymake" t)
  (defun flymake-pylint-init ()
    (let* ((temp-file (flymake-init-create-temp-buffer-copy
                       'flymake-create-temp-inplace))
           (local-file (file-relative-name
                        temp-file
                        (file-name-directory buffer-file-name))))
      (list "epylint" (list local-file))))

  (add-to-list 'flymake-allowed-file-name-masks
               '("\\.py\\'" flymake-pylint-init)))

;; (require 'pymacs)
;; (require 'pycomplete)
;; (autoload 'pymacs-load "ropemacs" "rope-")
;; (autoload 'pymacs-load "pymacs" nil t)
;; (autoload 'pymacs-eval "pymacs" nil t)
;; (autoload 'pymacs-apply "pymacs")
;; (autoload 'pymacs-call "pymacs")

;;(rope-init)

;; para autocompletar los cierres de parentesis o de string
;;(add-hook 'python-mode-hook
;;	  (lambda ()
;;	    (define-key python-mode-map "\"" 'electric-pair)
;;	    (define-key python-mode-map "\'" 'electric-pair)
;;	    (define-key python-mode-map "(" 'electric-pair)
;;	    (define-key python-mode-map "[" 'electric-pair)
;;	    (define-key python-mode-map "{" 'electric-pair)))

;;(defun electric-pair ()
;;  "Insert character pair without sournding spaces"
;;  (interactive)
;;  (let (parens-require-spaces)
;;    (insert-pair)))

;;;;;;;;;;
;; djcb ;;
;;;;;;;;;;
(defun djcb-opacity-modify (&optional dec)
  "modify the transparency of the emacs frame; if DEC is t,
    decrease the transparency, otherwise increase it in 10%-steps"
  (let* ((alpha-or-nil (frame-parameter nil 'alpha)) ; nil before setting
         (oldalpha (if alpha-or-nil alpha-or-nil 100))
         (newalpha (if dec (- oldalpha 10) (+ oldalpha 10))))
    (when (and (>= newalpha frame-alpha-lower-limit) (<= newalpha 100))
      (modify-frame-parameters nil (list (cons 'alpha newalpha))))))

;; C-8 will increase opacity (== decrease transparency)
;; C-9 will decrease opacity (== increase transparency
;; C-0 will returns the state to normal
(global-set-key (kbd "C-8") '(lambda()(interactive)(djcb-opacity-modify)))
(global-set-key (kbd "C-9") '(lambda()(interactive)(djcb-opacity-modify t)))
(global-set-key (kbd "C-0") '(lambda()(interactive)
                               (modify-frame-parameters nil `((alpha . 100)))))

;;;;;;;;;;;;;;;;;;;;;;
;; Quit this buffer ;;
;;;;;;;;;;;;;;;;;;;;;;
(defun quit-this-buffer ()
  "Exit current buffer by selecting some other buffer."
  (interactive)
  (switch-to-buffer (prog1 (other-buffer (current-buffer))
		      (bury-buffer (current-buffer)))))
(global-set-key "\C-cq" 'quit-this-buffer)

;;-> backspace on a selected region -> deletion
(delete-selection-mode t)

;;scroll line per line (1 line instead of 3)
(setq scroll-step 1)

;;display line and column number in toolbar
(setq line-number-mode t)
(setq column-number-mode t)

;;show_paren mode
(show-paren-mode t)

;; display clock
(display-time)

;; Use visible beel instead of beep
(setq visible-bell 't)

;;(dysplay question in 'y/n' instead of 'yes/no')
(fset 'yes-or-no-p 'y-or-n-p)

;; Save all my backup files in a specific directory
;(defun make-backup-file-name (file)
;  (concat "~/.autosave/" (file-name-nondirectory file)))
(setq backup-directory-alist
      `((".*" . ,temporary-file-directory)))
(setq auto-save-file-name-transforms
      `((".*" ,temporary-file-directory t)))
(windmove-default-keybindings)

(setq tramp-default-method "ssh")

(put 'upcase-region 'disabled nil)
(put 'downcase-region 'disabled nil)

;;; Prevent Extraneous Tabs
(setq-default indent-tabs-mode nil)
```


* Basic Configuration

```
;; to debug the .emacs file
(setq debug-on-error nil)

;; setup the default mode to use
;;Text mode is happier than Fundamental mode ;-)
(setq default-major-mode 'text-mode)

;; define the mail and name
(setq user-mail-address "foobar@example.com")
(setq user-full-name "Foo Bar")

;; define the ispell dictionary to use
(setq ispell-dictionary "en")

;; setup the tab to 4 spaces width
(setq tab-width 4)

(tool-bar-mode -1) ;; turn off toolbar
(scroll-bar-mode -1) ;; turn off scrollbar

;; color-theme
;; http://www.emacswiki.org/emacs/ColorTheme
;; http://www.nongnu.org/color-theme
(add-to-list 'load-path "~/.emacs.d/elisp/color-theme/")
(require 'color-theme)
(require 'color-theme-arjen)
(color-theme-arjen)

;; http://www.emacswiki.org/emacs/SwBuff
(require 'swbuff)
(global-set-key [(control tab)]       'swbuff-switch-to-next-buffer)
(global-set-key (kbd "<C-S-iso-lefttab>") 'swbuff-switch-to-previous-buffer)

(require 'whitespace)
(setq whitespace-style '(face empty tabs lines-tail trailing))
(add-hook 'python-mode-hook 'whitespace-mode)

;; Show tabs
(defface extra-whitespace-face
  '((t (:background "dim gray")))
  "Used for tabs and such.")
(defvar my-extra-keywords
  '(("\t" . 'extra-whitespace-face)))

(add-hook 'text-mode-hook
          (lambda () (font-lock-add-keywords nil my-extra-keywords)))

;; http://www.emacswiki.org/emacs/RectangleMark
(require 'rect-mark)
(global-set-key (kbd "C-x r C-SPC") 'rm-set-mark)
(global-set-key (kbd "C-x r C-x")   'rm-exchange-point-and-mark)
(global-set-key (kbd "C-x r C-w")   'rm-kill-region)
(global-set-key (kbd "C-x r M-w")   'rm-kill-ring-save)
```

* Python

```
;;;;;;;;;;;;
;; Python ;;
;;;;;;;;;;;;

(setq py-python-command "/usr/bin/python")

(setq auto-mode-alist (cons '("\\.py$" . python-mode) auto-mode-alist))
(setq interpreter-mode-alist (cons '("python" . python-mode)
                                   interpreter-mode-alist))
(autoload 'python-mode "python-mode" "Python editing mode." t)

;; show pydoc
;; http://www.emacswiki.org/cgi-bin/wiki/PythonMode
(defun my-python-documentation (w)
  "Launch PyDOC on the Word at Point"
  (interactive
   (list (let* ((word (thing-at-point 'word))
                (input (read-string
                        (format "pydoc entry%s: "
                                (if (not word) "" (format " (default %s)" word))))))
           (if (string= input "")
               (if (not word) (error "No pydoc args given")
                 word) ;sinon word
             input)))) ;sinon input
  (shell-command (concat py-python-command " -c \"from pydoc import help;help(\'" w "\')\"") "*PYDOCS*")
  (view-buffer-other-window "*PYDOCS*" t 'kill-buffer-and-window))

;;to show the pydoc help on the word at point
(add-hook 'python-mode-hook
          (function (lambda ()
                      (local-set-key [(control f1)] 'my-python-documentation)
                      )))

;;para indentar o completar con tab
(add-hook 'python-mode-hook
          (function (lambda ()
                      (local-set-key (kbd "<tab>") 'indent-or-complete)
                      )))
(add-hook 'python-mode-hook
          (function (lambda ()
                      (local-set-key (kbd "C-x #") 'comment-or-uncomment-region)
                      )))

;;pdb setup, note the python version
(setq pdb-path '/usr/bin/pdb
      gud-pdb-command-name (symbol-name pdb-path))
(defadvice pdb (before gud-query-cmdline activate)
  "Provide a better default command line when called interactively."
  (interactive
   (list (gud-query-cmdline pdb-path
                            (file-name-nondirectory buffer-file-name)))))

;; para usar pdb con F8
(add-hook 'python-mode-hook
          (function (lambda ()
                      (local-set-key (kbd "<f8>") 'pdb)
                      )))
;; para usar pydoc
(add-hook 'python-mode-hook
          '(lambda () (eldoc-mode 1)) t)

;;show tab in python mode
(add-hook 'python-mode-hook
          (lambda ()
            (font-lock-add-keywords nil my-extra-keywords)))

;; para mostrar el trailing whitespace
(add-hook 'python-mode-hook
          (lambda ()
            (setq show-trailing-whitespace t)))

;; usar pylint
(when (load "flymake" t)
  (defun flymake-pylint-init ()
    (let* ((temp-file (flymake-init-create-temp-buffer-copy
                       'flymake-create-temp-inplace))
           (local-file (file-relative-name
                        temp-file
                        (file-name-directory buffer-file-name))))
      (list "epylint" (list local-file))))

  (add-to-list 'flymake-allowed-file-name-masks
               '("\\.py\\'" flymake-pylint-init)))

;; (require 'pymacs)
;; (require 'pycomplete)
;; (autoload 'pymacs-load "ropemacs" "rope-")
;; (autoload 'pymacs-load "pymacs" nil t)
;; (autoload 'pymacs-eval "pymacs" nil t)
;; (autoload 'pymacs-apply "pymacs")
;; (autoload 'pymacs-call "pymacs")

;;(rope-init)

;; para autocompletar los cierres de parentesis o de string
;;(add-hook 'python-mode-hook
;;	  (lambda ()
;;	    (define-key python-mode-map "\"" 'electric-pair)
;;	    (define-key python-mode-map "\'" 'electric-pair)
;;	    (define-key python-mode-map "(" 'electric-pair)
;;	    (define-key python-mode-map "[" 'electric-pair)
;;	    (define-key python-mode-map "{" 'electric-pair)))

;;(defun electric-pair ()
;;  "Insert character pair without sournding spaces"
;;  (interactive)
;;  (let (parens-require-spaces)
;;    (insert-pair)))
```
