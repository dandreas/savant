#!/bin/sh
echo "Updating..."
git pull origin master
echo "Removing update file"
rm update.file
