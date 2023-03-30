Title: Org-mode and Beamer
Date: 2013-12-02

## Overview
The LaTeX class beamer allows production of high quality presentations using LaTeX and pdf processing. Org-mode has special support for turning an Org-mode file or tree into a beamer presentation. 

## Example
Here it is an example of how a presentation file should look like

    :::
    #+TITLE:     Org Mode and Beamer
    #+AUTHOR:    Felipe Reyes
    #+EMAIL:     freyes@tty.cl
    #+DATE:      2011-08-25 Tue
    #+DESCRIPTION:
    #+KEYWORDS:  org-mode, beamer, tutorial
    #+OPTIONS:   H:3 num:t toc:nil \n:nil @:t ::t |:t ^:t -:t f:t *:t <:t
    #+OPTIONS:   TeX:t LaTeX:t skip:nil d:nil todo:t pri:nil tags:not-in-toc
    #+INFOJS_OPT: view:nil toc:nil ltoc:nil mouse:underline buttons:0 path:http://orgmode.org/org-info.js
    #+EXPORT_SELECT_TAGS: export
    #+EXPORT_EXCLUDE_TAGS: noexport
    #+LINK_UP:   
    #+LINK_HOME: 
    #+LaTeX_CLASS: beamer
    #+BEAMER_HEADER_EXTRA: \usetheme{Madrid}\usecolortheme{default}
    #+MACRO: BEAMERMODE presentation
    #+MACRO: BEAMERINSTITUTE tty.cl
    #+BEAMER_FRAME_LEVEL: 2
    #+STARTUP: beamer
    
    * Org Mode and Beamer
    ** Overview
       - This is a bullet list
         - nested items
         - more items
       - Resume the top level list
    ** Numbered List
       1) one
       2) two
       3) three
    ** Source Code Example
    #+BEGIN_LaTeX
    \begin{lstlisting}[language=python]
    import os
    
    def my_fun(path="."):
        print os.listdir(path)
    \end{lstlisting}
    #+END_LaTeX

Let's review it by section

* First you just need to set the basic information about your presentation (title, author, email, date, description and keywords)
* Then you indicate if you want some extra options in each slide
* ``BEAMER_HEADER_EXTRA``: include raw LaTeX statements, this is used to define the beamer's theme, in this case we are using the theme *Madrid* with the *default* color theme.
* ``BEAMERMODE``: set the presentation mode in beamer
* ``BEAMERINSTITUTE``: let you define your college, business, etc.
* At the end we just write our slides, each level 2 section is a slide.

You can open the file [[file:org-mode.beamer.presentation.org]] in emacs and use the shortcut ``C-c C-e p`` to generate a pdf of the presentation. The produced pdf can be downloaded [[file:org-mode.beamer.presentation.pdf][here]]

## Setup

Execute the following command in Debian or Ubuntu

<pre>
sudo apt-get install texlive-extra-utils \
    texlive-binaries \
    latex-beamer \
    texlive-latex-extra
</pre>

Add the following to your *.emacs* file:

    :::lisp
    ;; beamer
    ;; #+LaTeX_CLASS: beamer in org files
    (unless (boundp 'org-export-latex-classes)
      (setq org-export-latex-classes nil))
    (add-to-list 'org-export-latex-classes
      ;; beamer class, for presentations
      '("beamer"
         "\\documentclass[11pt]{beamer}\n
          \\mode<{{{beamermode}}}>\n
          \\beamertemplateballitem\n
          \\setbeameroption{show notes}
          \\usepackage[utf8]{inputenc}\n
          \\usepackage[T1]{fontenc}\n
          \\usepackage{hyperref}\n
          \\usepackage{color}
          \\usepackage{listings}
          \\lstset{numbers=none,language=[ISO]C++,tabsize=4,
      frame=single,
      basicstyle=\\small,
      showspaces=false,showstringspaces=false,
      showtabs=false,
      keywordstyle=\\color{blue}\\bfseries,
      commentstyle=\\color{red},
      }\n
          \\usepackage{verbatim}\n
          \\institute{{{{beamerinstitute}}}}\n          
           \\subject{{{{beamersubject}}}}\n"
    
         ("\\section{%s}" . "\\section*{%s}")
         
         ("\\begin{frame}[fragile]\\frametitle{%s}"
           "\\end{frame}"
           "\\begin{frame}[fragile]\\frametitle{%s}"
           "\\end{frame}")))
    
    ;; letter class, for formal letters
    (add-to-list 'org-export-latex-classes
      '("letter"
         "\\documentclass[11pt]{letter}\n
          \\usepackage[utf8]{inputenc}\n
          \\usepackage[T1]{fontenc}\n
          \\usepackage{color}"
         
         ("\\section{%s}" . "\\section*{%s}")
         ("\\subsection{%s}" . "\\subsection*{%s}")
         ("\\subsubsection{%s}" . "\\subsubsection*{%s}")
         ("\\paragraph{%s}" . "\\paragraph*{%s}")
         ("\\subparagraph{%s}" . "\\subparagraph*{%s}")))

## Links

* [Beamer development repo](https://bitbucket.org/rivanvx/beamer/wiki/Home)
* [Worg beamer tutorial](http://orgmode.org/worg/org-tutorials/org-beamer/tutorial.html)
* [org-mode beamer](http://orgmode.org/manual/Beamer-class-export.html)
* [emacs-fu: writing presentations with org-mode and beamer](http://emacs-fu.blogspot.com/2009/10/writing-presentations-with-org-mode-and.html)
