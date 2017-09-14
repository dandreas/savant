#!/usr/bin/python3
import socket

# global vars
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
botnick = "savant" # nickname
server = "127.0.0.1" # default server
channel = "#default" # default channel

# functions
def setnick(name="savant"):
    """Bot nickname changing function.
    
    Changes the bot nickname.
    """
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
    while ircmsg.find("PING :") == -1 or count < 1000: # Attempts to register until the post-registration ping occurs.
        count += 1
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) # Fills out a form
        ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # assign the nick to the bot
        print(ircmsg)
        if ircmsg.find("PING :") != -1:
            print("(Connected to server.)")
            ping(ircmsg)
            

def joinchan(chan): # join channel(s)
    print("(Attempting to join channel: " + chan + ")")
    ircsock.send(bytes("JOIN " + chan + "\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def ping(msg): # respond to pings
    print("(Sending ping response...)")
    randstring = msg.split(':', 1)[1]
    ircsock.send(bytes("PONG :" + randstring + "\n", "UTF-8"))

def sendmsg(msg, target=channel): # sends a message to the target (if not defined, target is the channel)
    print("Sending:" + " (target): " + target + " (msg): " + msg)
    ircsock.send(bytes("PRIVMSG "+ target + " :" + msg + "\n", "UTF-8"))

def exitserver(): # ends the session with the current server
    ircsock.send(bytes("QUIT \n", "UTF-8"))