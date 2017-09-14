#!/usr/bin/python3
"""Savant Main Module

This module contains the entrypoint to savant. This module also handles plugins,
and parsing IRC data (determines which plugin/hard-coded action to execute given
the data recieved).

Attributes:
    adminname (string): Bot owner's username. The user with this name is given access to
        bot administrative commands such as the exitcode, or those set by plugins.
    exitcode (string): Text which is used in the exit command. Note that the user that
        sends this code MUST have the adminname variable as their nickname.
    pluginsatstart (class): Contains data about plugins installed for savant.

Todo:
    * ln
"""
# left off at ln70, which calls plugins.
import importlib
import pkgutil

import ircutils # contains functions for interacting with IRC servers

# global vars
adminname = "zauberin"
exitcode = "bye " + ircutils.botnick
pluginsatstart = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    if name.startswith('savant_')
}

def getplugins():
    """Plugin refresh function.

    Creates and fills a class with an updated list of plugins in the current directory, then returns it.

    Returns:
        plugins (class): The refreshed plugins class is returned.
            Normally is applied to the var plugins.
    """
    pluginlist = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name.startswith('savant_')
    }
    return pluginlist

def main():
    """Application entrypoint
    Runs the bot, listens to connections
    """
    server = input("Enter the IP address for the IRC server: ")
    channel = input("Enter the channel you would like to join: ")
    botnick = input("Enter the desired bot nickname: ")
    plugins = getplugins()

    ircutils.setnick(botnick)
    ircutils.connect(server)
    ircutils.joinchan(channel)
    
    while 1:
        # recieve IRC information, strip newlines/tabs
        ircmsg = ircutils.ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print("msg: " + ircmsg)

        # check if the info is a message / dm
        if ircmsg.find("PRIVMSG") != -1:
            # if the message is a dm / message, split the name and message contents into separate vars
            name = ircmsg.split('!', 1)[0][1:]
            message = ircmsg.split('PRIVMSG', 1)[1].split(':', 1)[1]

            # makes sure this is actually a message by authenticating name length
            if len(name) < 17:
                # commands
                if message[:8].find('.refresh') != -1:
                    ircutils.sendmsg("Plugins are being refreshed")
                    plugins = getplugins()
                # simple hello command
                if message.find('Hi ' + botnick) != -1:
                    ircutils.sendmsg("Hello " + name + "!")
                # instructs the bot to dm another user
                if message[:5].find('.tell') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in the format of: .tell [target] [message]"
                    ircutils.sendmsg(message, target)
                # plugin handle
                if message[:1] == '.':
                    pluginname = message.split(' ', 1)[0][1:]
                    print("command: " + pluginname)

                if name.lower() == adminname.lower() and message.rstrip() == exitcode:
                    ircutils.sendmsg("Shutting down...")
                    ircutils.exitserver()
                    return
        
        if ircmsg.find("PING :") != -1:
            ircutils.ping(ircmsg)

main() # starts the program
