#!/usr/bin/python3
"""IRC utilities for Savant.

This module handles most IRC functions for savant.Plugins can use this module to
edit various things about the IRC connection such as:
    The bot nickname
    Connect/disconnect to/from a server
    Join a channel

Attributes:
    ircsock (socket): Used to interact with an IRC server.
    botnick (string): The bot's nickname.
    server  (string): The IP address of the connected IRC server.
    channel (string): The default joined channel. The value of this variable
        does NOT reflect all connected channels.

"""
import socket

# global vars
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
botnick = "savant"
server = "127.0.0.1"
channel = "#default"

# functions
def setnick(name="savant"):
    """Bot nickname changing function.
    
    Changes the bot nickname.
    """
    global botnick # set with this function
    botnick = name

def connect(ircserver="127.0.0.1"): # connects to the server
    """IRC connection function.

    This function facilitates the initial connection to an IRC server.
    """
    server = ircserver # stores the currently connected server to a global var
    count = 0 # used to determine connection timeouts
    ircmsg = "" # stores input recieved from the irc server
    ircsock.connect((server, 6667)) # connect to the IRC server
    print("(Waiting for connection...)")
    while count < 1000: # Attempts to register until the post-registration ping occurs.
        count += 1 # when this hits 1000 the loop is auto cancelled.
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) # Fills out a form
        ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # assign the nick to the bot
        print(ircmsg) # debug stuff
        # check for the connection ping then exit
        if ircmsg.find("PING :") != -1:
            print("(Connected to server.)")
            ping(ircmsg)
            return # for some reason the loop wouldn't break without doing this
            

def joinchan(chan):
    """Join an IRC Channel.

    Args:
        chan (string): The name of the channel to be joined. The required # is added automatically.
        example: "default" joins "#default"

    """
    print("(Attempting to join channel: " + "#" + chan + ")")
    ircsock.send(bytes("JOIN " + "#" + chan + "\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if ircmsg.find("PING :") != -1:
            ping(ircmsg)
        print(ircmsg)

def ping(msg):
    """Ping responder.

    Sends a ping response according to the normal IRC format (PONG :{randomstring}).
    Normally, this will be managed by the main program, however if your plugin creates
    a new listening instance of it's own, you will need this in order to maintain connection
    to the IRC server.

    Args:
        msg (string): The raw message data that was detected to be a ping.
    """
    print("(sending ping response)")
    randstring = msg.split(':', 1)[1]
    ircsock.send(bytes("PONG :" + randstring + "\n", "UTF-8"))

def sendmsg(msg, target=channel):
    """Send an IRC Message.

    Sends a message to the target. If the target is not defined, sends a message to the default channel.

    Args:
        msg (string): The message to be sent to the target.
        target (string): The channel/user to send the message to.
    """
    print("sending:" + " (target): " + target + " (msg): " + msg)
    ircsock.send(bytes("PRIVMSG "+ target + " :" + msg + "\n", "UTF-8"))

def exitserver(): # ends the session with the current server
    """Exit the current server session.
    
    Exits the currently connected IRC server.
    """
    ircsock.send(bytes("QUIT \n", "UTF-8"))
