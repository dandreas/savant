#!/usr/bin/python3
"""Savant Channel Management

This plugin allows users to direct savant to join or leave a channel.
Can be admin restricted.
"""
import ircutils # not required, but allows manipulation of the connected IRC chat
# Required global variables
savantv = 0.000001
"""float: Savant Version.

Sets the plugin compatibility version. This is so that plugins do not break every
time a new required global variable is added to savant. Do not change this unless
you are sure your plugin meets the requirements of the specified version. Plugin API
info will soon be available on GitHub, until then this template file will be updated
to contain all required and optional variables to the most current version.
"""

# Required functions
def parse(rawmsg, name, message, subject):
    """Channel management call function

    Args:
        rawmsg (string): Full, unsullied string in which the pluginname call was detected
        name (string): The namespace (channel/user in case of pm) in which the call was detected
        message (string): The message which the user sent, the rest of the raw message is trimmed
        subject (string): The channel or user channel which the message was sent in
    """
    # The following code is an example plugin that simply joins a specified channel using ircutils
    if message != '.chan':
        command = message.split(' ', 1)[0][1] # trims '.chan'
        channel = message.split(' ', 2)[2]
        if command.lesser() == "join":
            ircutils.sendmsg("Attempting to join " + channel)
            ircutils.joinchan(channel)
        elif command.lesser() == "leave":
            ircutils.sendmsg("Attempting to leave " + channel)
            #TODO: add a leavechan function to ircutils
            #ircutils.leavechan(channel)
            
    else:
        ircutils.sendmsg("Commands: 'join [channel]', 'leave [channel]', 'restrict [channel]' (restricts leave command to admin for specified channel)", subject)