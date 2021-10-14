#!/usr/bin/env python3
from discord import Embed, Colour, Client, NotFound
from discord.ext import tasks

from secret import TOKEN

DEBUG = False

if DEBUG:
    SERVERID = 235478105177718785  # Foobar
    CHANNELID = 235478105177718785  # general
    MESSAGEFILE = 'message-debug.txt'
    try:
        with open(MESSAGEFILE, 'r') as f:
            MESSAGEID = int(f.read())
    except:
        MESSAGEID = 766695499532599316
else:
    SERVERID = 219564389462704130  # Zeus Operations
    CHANNELID = 287747328264372225  # welcome
    try:
        with open(MESSAGEFILE, 'r') as f:
            MESSAGEID = int(f.read())
    except:
        MESSAGEID = 766703178082287616


client = Client()
URL = "https://banner.zeusops.com/image/banner.png?q={}"
if DEBUG:
    URL=f"{URL}&rainbow"
with open('number.txt', 'r') as f:
    try:
        number = int(f.read())
    except:
        number = 983
message = None


@tasks.loop(seconds=15)
async def update():
    global number
    global message
    number += 1
    with open('number.txt', 'w') as f:
        f.write(str(number))
    if message:
        await message.edit(content=URL.format(number))

@client.event
async def on_ready():
    global message
    server = client.get_guild(SERVERID)
    channel = server.get_channel(CHANNELID)

    try:
        message = await channel.fetch_message(MESSAGEID)
    except NotFound:
        message = await channel.send(URL.format(number))
        with open(MESSAGEFILE, 'w') as f:
            f.write(str(message.id))
    else:
        await message.edit(content=URL.format(number))

    update.start()

if __name__ == "__main__":
    client.run(TOKEN)

