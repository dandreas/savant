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

Todo:
    * project:
        * Make a default plugin for downloading plugins via the bot.
        * Make the savant_oper.py plugin for advanced admin stuff
        * Make the werewolf.py and dependencies as a test plugin.
        * Make a configuration file for savant to store server, botnick, and default channel
        * Fix remote updating. Git command probably just needs to be put in update.sh and update.sh run from a
        subprocess.call
        * Update the pydoc attributes on all modules.
        * (long-term) Add discord support
        * Make the update function check the install.file for whether it says 'win' or 'nix' to determine which update
        script to run.
    * main():
        * Arg handling needs to be cleaned
        * Plugins need to be printed in the default '.help' command
"""
# import importlib  # for future plugin management. not used
# import pkgutil  # also for future plugin management. not used
import sys  # used to get command line args
# from subprocess import call  # used for remote update (not anymore due to issues)
import os  # used for finding plugins

import ircutils  # contains functions for interacting with IRC servers

installed = False  # used to verify installation

# checks to see if savant has been installed
try:
    file = open("install.file", "r+")
    file.close()
    installed = True
except FileNotFoundError as p:
    print("Savant is not installed!\nRun 'install.sh' to remedy this")

# global vars
adminname = "zauberin"
exitcode = ircutils.botnick + " shutdown"
plugins = []  # written in get_plugins()
sys.path.append("../plugins")  # adds the plugin directory to pythons path


# makes a list of plugins.
# this list is comprehensive of all of the possible callable plugins
def get_plugins():
    global plugins  # written here.
    print("\n(checking for plugins)")
    for root, dirs, files in os.walk("../plugins"):
        for file_ in files:
            if file_.startswith("savant_"):
                plugin = str(file_).split('_', 1)[1]
                plugin = plugin.split('.', 1)[0]
                plugins.append(plugin)
    for i in range(len(plugins)):
        print(str(plugins[i]))


# temporary function for loading plugins
def load_plugin(pluginName):
    print("(searching for plugin)")
    for i in range(len(plugins)):
        if str(plugins[i]).find(pluginName) != -1:
            mod = __import__("savant_%s" % pluginName)
            return mod
        else:
            return 1


# temporary function for calling plugins
def call_plugin(pluginName, rawmsg, name, message, subject):
    plugin = load_plugin(pluginName)
    if plugin != 1:
        try:
            plugin.parse(rawmsg, name, message, subject)
        except Exception as x:
            print(str(x))
            ircutils.sendmsg("Plugin " + pluginName + " encountered an error.")
        return 0
    else:
        return 1


""" Should be re-implemented in the future.
Make sure to restore comments in getplugins() function.

pluginsatstart = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    if name.startswith('savant_')
}

def getplugins():
    "\""Plugin refresh function.

    Creates and fills a class with an updated list of plugins in the current directory, then returns it.

    Returns:
        plugins (class): The refreshed plugins class is returned.
            Normally is applied to the var plugins.
    "\""
    pluginlist = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name.startswith('savant_')
    }
    return pluginlist
"""


def main():
    """Application entrypoint
    Runs the bot, listens to connections
    """
    server = "127.0.0.1"
    channel = "default"
    botnick = "savant"

    # TODO clean this up
    if len(sys.argv) != 1:
        for i in range(len(sys.argv)):
            if sys.argv[i] == '-s':
                server = str(sys.argv[i+1])
            if sys.argv[i] == '-c':
                channel = str(sys.argv[i+1])
            if sys.argv[i] == '-n':
                botnick = str(sys.argv[i+1])
            if sys.argv[i] == '-h':
                print("Usage: savant.py [COMMAND] [VALUE] [...]\n'-s' = server IP\n'-c' = channel\n'-n' = botnick " +
                      "(note botnicks set by command line must not have spaces)")
    else:
        server = input("Enter the IP address for the IRC server: ")
        channel = input("Enter the channel you would like to join: ")
        botnick = input("Enter the desired bot nickname: ")
    
    # plugins = getplugins() # used in importlib plugin handle
    
    # joins the server and channel set
    ircutils.setnick(botnick)
    ircutils.connect(server)
    ircutils.joinchan(channel)
    # gets the plugin list
    get_plugins()

    # print bot and server data
    print("\nbotnick  : " + botnick)
    print("server IP: " + server)
    print("channel  : " + channel)
    
    while 1:
        # recieve IRC information, strip newlines/tabs
        ircmsg = ircutils.ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print("\nmsg: " + ircmsg)
        command = False  # used to check if a default command was used

        # check if the info is a message / dm
        if ircmsg.find('PRIVMSG') != -1:
            # if the message is a dm / message, split the name and message contents into separate vars
            name = ircmsg.split('!', 1)[0][1:]
            message = ircmsg.split('PRIVMSG', 1)[1].split(':', 1)[1]
            subject = ircmsg.split('PRIVMSG', 1)[1].split(':', 1)[0]
            subject = subject.strip(' ')
            # sets subject to sender if its a dm
            if subject == botnick:
                subject = name

            print("(PRIVMSG)")
            print("name: " + name + "\nmessage: " + message + "\nchannel: " + subject)

            # makes sure this is actually a message by authenticating name length
            if len(name) < 17:
                # commands
                # list commands
                if message[:5].lower().find('.help') != -1:
                    command = True
                    ircutils.sendmsg("Possible commands:")
                    ircutils.sendmsg("defaults: '.update', '.refresh', '.tell', '.help'")
                    # prints off available plugins
                    ircutils.sendmsg("plugins: ")
                    pliststr = []
                    ct = 0
                    for plugin in plugins:
                        pliststr.append(str(plugin))
                        ct += 1
                        if ct > 20:
                            pstrfull = ""
                            for pstr in pliststr:
                                pstrfull += pstr + ' '
                            ircutils.sendmsg(pstrfull)
                            ct = 0
                            pliststr.clear()
                    if ct > 0:
                        pstrfull = ""
                        for pstr in pliststr:
                            pstrfull += pstr + ' '
                        ircutils.sendmsg(pstrfull)
                        ct = 0
                # /if message[:5].lower().find('.help') != -1:
                # attempt an update
                if message[:7].find('.update') != -1:
                    command = True
                    if name.lower() == adminname.lower():
                        ircutils.sendmsg("Updating...")
                        os.system("./update.sh")  # updates savant
                        ircutils.sendmsg("Update finished! Shutting down...")
                        return
                    else:
                        ircutils.sendmsg("Insufficient permissions")
                # refreshes plugins
                if message[:8].find('.refresh') != -1:
                    command = True
                    ircutils.sendmsg("Plugins are being refreshed")
                    get_plugins()
                    ircutils.sendmsg("Plugins refreshed! Use the command '.help' to get a list of active plugins")
                # simple hello command
                if message.lower().find('hi ' + botnick) != -1:
                    command = True
                    ircutils.sendmsg("Hello " + name + "!", subject)
                # instructs the bot to dm another user
                if message[:5].find('.tell') != -1:
                    command = True
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in the format of: .tell [target] [message]"
                    ircutils.sendmsg(message, target)
                # plugin handle
                # "temporary" plugin handle
                if message[:1] == '.':
                    # Just prints the command
                    pluginName = message.split(' ', 1)[0][1:]
                    print("command: " + pluginName)
                    retval = call_plugin(pluginName, ircmsg, name, message, subject)
                    # if no default commands were called and no plugins were found, notify the user.
                    if retval == 1 and command is False:
                        ircutils.sendmsg("Plugin '" + pluginName + "' not found")
                
                """ For when importlib is implemented
                if message[:1] == '.':
                    pluginname = message.split(' ', 1)[0][1:]
                    print("command: " + pluginname)
                """

                # remote shutdown command
                if name.lower() == adminname.lower() and message.rstrip().lower() == exitcode.lower():
                    ircutils.sendmsg("Shutting down...")
                    ircutils.exitserver()
                    return
            # /if len(name) < 17:
        if ircmsg.find("PING :") != -1:
            ircutils.ping(ircmsg)
    # /while 1:
# /main()


if installed:
    main()  # starts the program
