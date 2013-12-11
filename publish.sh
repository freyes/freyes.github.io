#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh
workon peli
pelican -s pelicanconf.py -o output/
pushd output
git add .
git commit -m "new publication"
git push origin master
popd
git add output
git commit -m "updated blog"
