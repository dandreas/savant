#!/bin/sh
echo "Creating plugins directory..."
mkdir ../plugins
echo "Moving default plugins..."
cp savant_chan.py ../plugins
echo "Removing update file"
rm update.file
echo "1" > install.file
echo "Installation complete!"