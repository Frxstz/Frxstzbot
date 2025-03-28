"""
Queue script made for integrating two chats into one "chat.log" File.
Added Raffle like 2 years later
Authors: frxstz on discord
         bop on discord

Dependencies: 
- Python3
- pip (usually installed with python)
- emoji (use "python -m pip install emoji --upgrade")
"""

import socket
from emoji import demojize
import logging
import os
from datetime import datetime


queue_list       = []
DIR              = os.getcwd()
server           = 'irc.chat.twitch.tv'
port             = 6667
nickname         = 'frostqbot'
path = os.path.join(DIR,'quebotV1','settings','token.txt')
with open(path, "r") as f:
    token = f.read().splitlines()
token = token[0]
queueFile        = 'queue.txt'
raffleFile       = 'raffle.txt'
userQueueFile    = 'userqueue.txt'
userRaffleFile   = 'userraffle.txt'
channelQueueFile = 'channelqueue.txt'
channelRaffleFile= 'channelraffle.txt'
queueBots, channels, joinQueue, pullQueue, leaveQueue, skipQueue, joinRaffle, pullRaffle, leaveRaffle = [], [], [], [], [], [], [], [], []

with open("chat.log", 'w') as f:
    pass


# Gets the context lists for each instance of the bot actions. 
# #Think of contexts as commands. WIthout them, this bot doesnt 
# # know what to do
def GetContextFileInfo():
    global queueBots, channels, joinQueue, pullQueue, leaveQueue, skipQueue, joinRaffle, pullRaffle, leaveRaffle
    path = os.path.join(DIR,'quebotV1','settings','queuebots.txt')
    with open(path, "r") as f:
        queueBots = f.read().splitlines()
    path = os.path.join(DIR,'quebotV1','settings','channels.txt')
    with open(path, "r") as f:
        channels = f.read().splitlines()
    path = os.path.join(DIR,'quebotV1','settings','context_files','joinedqueuecontext.txt')
    with open(path, "r") as f:
        joinQueue = f.read().splitlines()
    path = os.path.join(DIR,'quebotV1','settings','context_files','pullqueuecontext.txt')
    with open(path, "r") as f:
        pullQueue = f.read().splitlines()
    path = os.path.join(DIR,'quebotV1','settings','context_files','skipqueuecontext.txt')
    with open(path, "r") as f:
        skipQueue = f.read().splitlines()
    path = os.path.join(DIR,'quebotV1','settings','context_files','leavequeuecontext.txt')
    with open(path, "r") as f:
        leaveQueue = f.read().splitlines()
        #newcode
    path = os.path.join(DIR,'quebotV1','settings','context_files','joinedrafflecontext.txt')
    with open(path, "r") as f:
        joinRaffle = f.read().splitlines()
    path = os.path.join(DIR,'quebotV1','settings','context_files','pullrafflecontext.txt')
    with open(path, "r") as f:
        pullRaffle = f.read().splitlines()
    path = os.path.join(DIR,'quebotV1','settings','context_files','leaverafflecontext.txt')
    with open(path, "r") as f:
        leaveRaffle = f.read().splitlines()
    

# Parses out the user from the chat response. Depends on the 
# user being '@' in chat in order to correctly locate the correct user
def GetUser(response):
    username = response.split('@')[-1]
    username = (username.split()[0]).split(',')[0]
    return username

# Parses out the streamer from the chat response. 
def GetChannelOfUser(response):
    chnlOfUser = response.split('#')[-1]
    chnlOfUser = chnlOfUser.split()[0]
    return chnlOfUser

# Determines the index in a list where a substring is located regardless of case
def IndexContainingSubstring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring.lower() in s.lower():
            return i
    return -1

# Given a file, data, and type (where type is 'r', 'w' aka fil actions) 
# # writes to the file
def ToFile(file, data, type):
    with open(file, type) as file1:
        file1.write(data)
    



# use queue.txt to fill in the userqueue & channelqueue txt files if data exists
path = os.path.join(DIR,'quebotV1','queue.txt')
with open(path, 'r') as f1:
    with open("userqueue.txt", 'w') as f2:
        with open("channelqueue.txt", 'w') as f3:
            queue = f1.read().splitlines()
            for q in queue:
                f2.write(q.split(' - ')[0] + '\n')
                f3.write(q.split(' - ')[1] + '\n')

# use raffle.txt to fill in the userraffle & channelraffle txt files if data exists
path = os.path.join(DIR,'quebotV1','raffle.txt')
with open(path, 'r') as f1:
    with open("userraffle.txt", 'w') as f2:
        with open("channelraffle.txt", 'w') as f3:
            queue = f1.read().splitlines()
            for q in queue:
                f2.write(q.split(' - ')[0] + '\n')
                f3.write(q.split(' - ')[1] + '\n')



GetContextFileInfo() # gather context lists for use below

# SOME QUICK VALIDATION
if not len(channels):
    print("FAILURE - The channels.txt file is empty! This must have at least 1 channel. See README for more information.")
    exit()

if not len(queueBots):
    print("FAILURE - The queuebots.txt file is empty! This must have at least 1 username. See README for more information.")
    exit()

if not len(joinQueue):
     print("WARNING! - joinqueuecontext.txt is empty. Join Queue operations will be unsuccessful. See README for more information.")

if not len(pullQueue):
     print("WARNING! - pullqueuecontext.txt is empty. Pull Queue operations will be unsuccessful. See README for more information.")

if not len(leaveQueue):
     print("WARNING! - leavequeuecontext.txt is empty. Leave Queue operations will be unsuccessful. See README for more information.")

if not len(skipQueue):
     print("WARNING! - skipqueuecontext.txt is empty. Skip Queue operations will be unsuccessful. See README for more information.")

if not len(joinRaffle):
     print("WARNING! - joinrafflecontext.txt is empty. Join raffle operations will be unsuccessful. See README for more information.")

if not len(pullRaffle):
     print("WARNING! - pullrafflecontext.txt is empty. Pull raffle operations will be unsuccessful. See README for more information.")

if not len(leaveRaffle):
     print("WARNING! - leaverafflecontext.txt is empty. Leave raffle operations will be unsuccessful. See README for more information.")


sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
chnloutput = '\n-------------------\nConnected Twitch Chats: '
for chnl in channels:
    chnloutput += '\n'+chnl
    sock.send(f"JOIN {'#'+chnl}\n".encode('utf-8'))
print(chnloutput)
print("\n-------------------\nUsers Bot is authorized to interpret:")
for u in queueBots:
    print(u)
resp = sock.recv(2048).decode('utf-8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

logging.info(resp)
print("\nQueue established. Bot is Successfully running.. ...\n----\n----\n")



# like a server. Here is where we wait for messages to hit the twitch chats
# of the users in the channels.txt file
while True:
    resp = sock.recv(2048).decode('utf-8')
    print(resp)

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))

    elif len(resp) > 0:
        logging.info(demojize(resp))
        try:
            GetContextFileInfo()
            # parse out the user in the message
            messenger = resp.split('!')[0][1:]
            #check if messenger is one of the possible bots responsible for queue changes
            if messenger in queueBots:

                #kill the queue bot
                if "is now closed!!" in resp:
                    print("Bot has been shut down successfuly")
                    exit()

                # clear the queue files
                if "queue has been cleared!!" in resp:
                    with open(queueFile, 'w') as f:
                        pass 
                    with open(channelQueueFile, 'w') as f:
                        pass
                    with open(userQueueFile, 'w') as f:
                        pass 
                    print("Queue files have been cleared... ...")

                # clear the raffle files
                if "raffle has been cleared!!" in resp:
                    with open(raffleFile, 'w') as f:
                        pass 
                    with open(channelRaffleFile, 'w') as f:
                        pass
                    with open(userRaffleFile, 'w') as f:
                        pass 
                    print("Raffle files have been cleared... ...")

                # MAIN LOGIC
                # There are 7 blocks below
                # - Join Block - handle user joining the queue
                # - Pull Block - handle user being pulled from the queue
                # - Leave Block - handle user leaving the queue voluntarily
                # - Skip Block - handle a player whose turn will be skipped in the queue
                # RAFFLE BLOCKS
                # - Join Block - handle user joining the raffle
                # - Pull Block - handle a user being randomly pulled from the raffle
                # - Leave Block - handle user leaving the raffle voluntarily
                for j in joinQueue:
                    if (j in resp) and ('@' in resp.split("tmi.twitch.tv")[1]):
                        user = GetUser(resp)
                        channelOfUser = GetChannelOfUser(resp)
                        now = datetime.now().strftime("%I:%M:%S%p %Z")
                        # Writing to files
                        ToFile(queueFile, user+" - "+channelOfUser+" - "+now+"\n", "a")
                        ToFile(userQueueFile, user+"\n", "a")
                        ToFile(channelQueueFile, channelOfUser+"\n", "a")
                        print(user + ' has been added to the queue file')
                        break

                for p in pullQueue:
                    if (p in resp) and ('@' in resp.split("tmi.twitch.tv")[1]):
                        user = GetUser(resp)
                        with open(queueFile, "r") as f:
                            qlines = f.readlines()
                        with open(userQueueFile, "r") as f:
                            uqlines = f.readlines()                        
                        with open(channelQueueFile, "r") as f:
                            chqlines = f.readlines()
                        qOutputString, uqOutputString, chqOutputString = '', '', ''
                        for i in range(0, len(qlines)):
                            if user.lower() != uqlines[i].lower().strip("\n"):
                                qOutputString = qOutputString + qlines[i]
                                uqOutputString = uqOutputString + uqlines[i]
                                chqOutputString = chqOutputString + chqlines[i]
                        ToFile(queueFile, qOutputString, "w")
                        ToFile(userQueueFile, uqOutputString, "w")
                        ToFile(channelQueueFile, chqOutputString, "w")
                        print(user + ' has been pulled from the queue file')
                        break

                for l in leaveQueue:
                    if (l in resp) and ('@' in resp.split("tmi.twitch.tv")[1]):
                        user = GetUser(resp)
                        with open(queueFile, "r") as f:
                            qlines = f.readlines()
                        with open(userQueueFile, "r") as f:
                            uqlines = f.readlines()                        
                        with open(channelQueueFile, "r") as f:
                            chqlines = f.readlines()
                        qOutputString, uqOutputString, chqOutputString = '', '', ''
                        for i in range(0, len(qlines)):
                            if user.lower() != uqlines[i].lower().strip("\n"):
                                qOutputString = qOutputString + qlines[i]
                                uqOutputString = uqOutputString + uqlines[i]
                                chqOutputString = chqOutputString + chqlines[i]
                        ToFile(queueFile, qOutputString, "w")
                        ToFile(userQueueFile, uqOutputString, "w")
                        ToFile(channelQueueFile, chqOutputString, "w")
                        print(user + ' has been removed from the queue file')
                        break

                for s in skipQueue:
                    if (s in resp) and ('@' in resp.split("tmi.twitch.tv")[1]):
                        # user has joined queue
                        user = GetUser(resp)
                        with open(queueFile, "r") as f:
                            qlines = f.readlines()
                        with open(userQueueFile, "r") as f:
                            uqlines = f.readlines()                        
                        with open(channelQueueFile, "r") as f:
                            chqlines = f.readlines()
                        qOutputString, uqOutputString, chqOutputString = '', '', '' 

                        try:
                            index = IndexContainingSubstring(uqlines, user)
                        except:
                            print(user, "is not in the queue")
            
                        userChannelToBeMoved = qlines[index]
                        userChannelInNextPosition = qlines[index + 1]
                        qlines[index] = userChannelInNextPosition
                        qlines[index + 1] = userChannelToBeMoved

                        userToBeMoved = uqlines[index]
                        userInNextPosition = uqlines[index + 1]
                        uqlines[index] = userInNextPosition
                        uqlines[index + 1] = userToBeMoved

                        channelToBeMoved = chqlines[index]
                        channelInNextPosition = chqlines[index + 1]
                        chqlines[index] = channelInNextPosition
                        chqlines[index + 1] = channelToBeMoved

                        for i in range(0, len(qlines)):
                            qOutputString = qOutputString + qlines[i]
                            uqOutputString = uqOutputString + uqlines[i]
                            chqOutputString = chqOutputString + chqlines[i]    
                        
                        ToFile(queueFile, qOutputString, "w")
                        ToFile(userQueueFile, uqOutputString, "w")
                        ToFile(channelQueueFile, chqOutputString, "w") 
                                    
                        print(user + ' has been moved down one slot in the queue')
                        break

                # Raffle Blocks
                for jr in joinRaffle:
                    if (jr in resp) and ('@' in resp.split("tmi.twitch.tv")[1]):
                        user = GetUser(resp)
                        channelOfUser = GetChannelOfUser(resp)
                        now = datetime.now().strftime("%I:%M:%S%p %Z")
                        # Writing to files
                        ToFile(raffleFile, user+" - "+channelOfUser+" - "+now+"\n", "a")
                        ToFile(userRaffleFile, user+"\n", "a")
                        ToFile(channelRaffleFile, channelOfUser+"\n", "a")
                        print(user + ' has been added to the raffle file')
                        break

                for lr in leaveRaffle:
                    if (lr in resp) and ('@' in resp.split("tmi.twitch.tv")[1]):
                        user = GetUser(resp)
                        with open(raffleFile, "r") as f:
                            rlines = f.readlines()
                        with open(userRaffleFile, "r") as f:
                            urlines = f.readlines()                        
                        with open(channelRaffleFile, "r") as f:
                            chrlines = f.readlines()
                        rOutputString, urOutputString, chrOutputString = '', '', ''
                        for i in range(0, len(rlines)):
                            if user.lower() != urlines[i].lower().strip("\n"):
                                rOutputString = rOutputString + rlines[i]
                                urOutputString = urOutputString + urlines[i]
                                chrOutputString = chrOutputString + chrlines[i]
                        ToFile(raffleFile, rOutputString, "w")
                        ToFile(userRaffleFile, urOutputString, "w")
                        ToFile(channelRaffleFile, chrOutputString, "w")
                        print(user + ' has been removed from the raffle file')
                        break

                for pr in pullRaffle:
                    if (pr in resp) and ('@' in resp.split("tmi.twitch.tv")[1]):
                        user = GetUser(resp)
                        with open(raffleFile, "r") as f:
                            rlines = f.readlines()
                        with open(userRaffleFile, "r") as f:
                            urlines = f.readlines()                        
                        with open(channelRaffleFile, "r") as f:
                            chrlines = f.readlines()
                        rOutputString, urOutputString, chrOutputString = '', '', ''
                        for i in range(0, len(rlines)):
                            if user.lower() != urlines[i].lower().strip("\n"):
                                rOutputString = rOutputString + rlines[i]
                                urOutputString = urOutputString + urlines[i]
                                chrOutputString = chrOutputString + chrlines[i]
                        ToFile(raffleFile, rOutputString, "w")
                        ToFile(userRaffleFile, urOutputString, "w")
                        ToFile(channelRaffleFile, chrOutputString, "w")
                        print(user + ' has been removed from the raffle file (won the raffle)')
                        break
        except:
            print("ERROR/////", resp)


