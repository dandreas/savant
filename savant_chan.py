#!/usr/bin/python3
"""Savant Channel Management

This plugin allows users to direct savant to join or leave a channel.
Can be admin restricted.
"""
import ircutils
import savant
# Required global variables
savantv = 0.000001
"""float: Savant Version.

Sets the plugin compatibility version. This is so that plugins do not break every
time a new required global variable is added to savant. Do not change this unless
you are sure your plugin meets the requirements of the specified version. Plugin API
info will soon be available on GitHub, until then this template file will be updated
to contain all required and optional variables to the most current version.
"""
rchans = [ircutils.channel]

def parse(rawmsg, name, message, subject):
    """Channel management call function

    Args:
        rawmsg (string): Full, unsullied string in which the pluginname call was detected
        name (string): The namespace (channel/user in case of pm) in which the call was detected
        message (string): The message which the user sent, the rest of the raw message is trimmed
        subject (string): The channel or user channel which the message was sent in
    """
    global rchans
    if message != '.chan':
        # Split the command and arg from the message
        command = message.split(' ', 2)[0][1] # trims '.chan'
        channel = message.split(' ', 2)[2]
        print("command: " + command + "\nchannel: " + channel)
        # Determine which command was used
        if command.lesser() == "join": # joins a specified channel
            ircutils.sendmsg("Attempting to join " + channel)
            ircutils.joinchan(channel)
        elif command.lesser() == "leave": # leaves the specified channel
            ircutils.sendmsg("Attempting to leave " + channel)
            if channel in rchans == True: # makes sure savant is actually in that channel
                if 'oper' in savant.plugins == True:
                    #TODO fill this in when oper is finished.
                    print("(chan: no special oper stuff yet)")
                    if name == savant.adminname:
                        ircutils.leavechan(channel)
                else:
                    if name == savant.adminname:
                        ircutils.leavechan(channel)
        elif command.lesser() == "restrict": # restrict leaving this channel to 
            ircutils.sendmsg("Restriction added for channel: #" + channel)
            rchans.append(channel)
        elif command.lesser() == "ur":
            ircutils.sendmsg("Restriction removed for channel: #" + channel)
            try:
                rchans.remove(channel)
            except ValueError as ex:
                ircutils.sendmsg("#" + channel + " is not restricted!")
            
    else:
        ircutils.sendmsg("Commands: 'join [channel]', 'leave [channel]', 'restrict [channel]' (restricts leave command to admin for specified channel), ur [channel] (unrestricts specified channel)", subject)