#!/usr/bin/python3
"""Savant Plugin Template.

This module is a basic template demonstrating the required variables/functions to creating a
savant plugin.
"""
import ircutils # not required, but allows manipulation of the connected IRC chat
# Required global variables
# note: savantv isn't read yet, 0.000001 is simply a placeholder for 'no gvs'
savantv = 0.000001
"""float: Savant Version.

Sets the plugin compatibility version. This is so that plugins do not break every
time a new required global variable is added to savant. Do not change this unless
you are sure your plugin meets the requirements of the specified version. Plugin API
info will soon be available on GitHub, until then this template file will be updated
to contain all required and optional variables to the most current version.
"""

# Required functions
def parse(rawmsg, name, message):
    """Parse API call function.

    This function is called by savant when the following conditions are met:
        The filename for this plugin is valid (savant_{pluginname}.py)
        A user in a channel savant is listening to sends a message beginning with '.{pluginname}'
    Note that the code below is merely an example plugin, and not necessary

    Args:
        rawmsg (string): Full, unsullied string in which the pluginname call was detected
        name (string): The namespace (channel/user in case of pm) in which the call was detected
        message (string): The message which the user sent, the rest of the raw message is trimmed
    """
    # The following code is an example plugin that simply joins a specified channel using ircutils
    if message != '.plugintemplate':
        channel = message.split(' ', 1)[0][1:] # trims '.plugintemplate'
        ircutils.joinchan(channel)
        ircutils.sendmsg("Attempting to join " + channel)
    else:
        ircutils.joinchan("#test")
        ircutils.sendmsg("Attempting to join #test",name)