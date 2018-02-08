#!/bin/sh
echo "Creating plugins directory..."
mkdir ../plugins
echo "Moving default plugins..."
cp savant_chan.py ../plugins
cp savant_oper.py ../plugins
echo "Removing update file"
rm update.file
echo "nix" > install.file
echo "Installation complete!"