#!/usr/bin/python3
"""Savant oper extension

Adds a few new functionalities to Savant:
    1. An admin list: Instead of the single default admin, you can now have several. You can also add to this list via the plugin.
    2. Lobby permissions: Savant can create a lobby as oper and allow admins to administrate by proxy. Non-admins have 'admin' privileges in lobbies they create.
    3. Vote kicks: Non-admins can start a vote for channel kicks of other non-admins

ToDo list:
    * 
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
    """Savant oper extension

    Adds a few new functionalities to Savant:
    1. An admin list: Instead of the single default admin, you can now have several. You can also add to this list via the plugin.
    2. Lobby permissions: Savant can create a lobby as oper and allow admins to administrate by proxy. Non-admins have 'admin' privileges in lobbies they create.
    3. Vote kicks: Non-admins can start a vote for channel kicks of other non-admins
    
    Args:
        rawmsg (string): Full, unsullied string in which the pluginname call was detected
        name (string): The namespace (channel/user in case of pm) in which the call was detected
        message (string): The message which the user sent, the rest of the raw message is trimmed
        subject (string): The channel or user channel which the message was sent in
    """
    # The following code is an example plugin that simply joins a specified channel using ircutils
    if message != '.oper':
        commands = message.split(' ',1)[0][1:] # trims '.plugintemplate'
        if commands[:4].find('help') != -1:
            ircutils.sendmsg("Commands: 'help', 'vote [name]', 'join [channel]', 'ml' (make lobby), 'add' (add admin(admin only)), 'rm' (remove admin(admin only)), 'mod' (add moderator(admin only)), 'rmod'", subject)
        if commands[:4].find('vote') != -1:
            kickee = message.split(' ',1)[0][1:]
            ircutils.sendmsg("votekick called for:" + kickee)
    else:
        ircutils.sendmsg("Commands: 'help', 'vote [name]', 'join [channel]', 'ml' (make lobby), 'add' (add admin(admin only)), 'rm' (remove admin(admin only)), 'mod' (add moderator(admin only)), 'rmod'", subject)