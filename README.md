Thanks for using Frxstzbot!
Frxstzbot is a MCQB (Multi-Chat queue bot), we are still in early stages but we feel that we have a good enough product to have it useable.
Frxstzbot is to be used with streamerbot (https://streamer.bot/). The way bop has been using it, is as a channel point reward, streamerbot would pick that up and then say something in chat. For example if the viewer hit the "join queue" reward, streamerbot would respond with "@viewer has joined the queue" (or whatever you set it to inside streamerbot). That message from streamerbot would then get picked up by the python bot. 

In the settings folder of the bot there are two files you can edit, one called channels, the other called queuebots.

channels.txt must have at least 1 channel in it or else the bot will break, same with queuebots.txt. That being said we have tested this with 3 channels. We gave not seen the limit on channels yet. 

CHECK NO WRAP / RAW FILE FOR PROPER EXAMPLE OF CHANNELS.TXT & QUEUEBOTS.TXT

channels.txt - The channels you wish to use for the bot, place them with no skipped lines and case sensitive, Ex.
frxstz_
itisbop
Krausader

queuebots.txt - These are the accounts that have influence on adding / removing people from queue (queue.txt), If you want, you can even add mods to this list, also place them with no skipped lines and case sensitive, Ex.
frxstz_
frxstz_bot
itisbop
pat_the_spade
Krausader
lord_salad_bot

Inside context_files you will find the context of actions performed by channel points that your streamerbot will respond to. These files are loaded with examples and are self explanatory. In these files you will add your context as well as your co-streamers.
We do not endorse / encourage using Frxstzbot in chats that you dont have permission directly from the broadcaster in. 

All this bot does is read chat, it does not send any data in the backend or anything like that. The idea is to have you running the bot and your friend you want to combine queues with also running the bot, reading each others chat with the same settings. Its done this way to avoid needing to send data over discord.

In the zip is a start.bat file you should use to start the frxstzbot.exe file. There is also a frxstzbot.py file, this is source python file since this is an open source project.  
