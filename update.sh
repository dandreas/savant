#!/bin/sh
echo "Updating..."
git pull origin master
yes | cp -rf savant_oper.py ../plugins
yes | cp -rf savant_chan.py ../plugins
echo "Removing update file"
rm update.file
