#!/bin/sh
echo "Creating plugins directory..."
mkdir ../plugins
echo "Moving default plugins..."
cp savant_plugintemplate.py ../plugins
mv ../plugins/savant_plugintemplate.py ../plugins/savant_joinchan.py
echo "Removing update file"
rm update.file
echo "1" > install.file
echo "Installation complete!"