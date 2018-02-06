echo "Creating plugins directory..."
md ../plugins
echo "Moving default plugins..."
cp savant_chan.py ../plugins
echo "Removing update file"
del update.file
echo "win" > install.file
echo "Installation complete!"