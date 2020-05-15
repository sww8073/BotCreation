# bot.py
# A simple Discord bot for polls
import os
import discord
from dotenv import load_dotenv, find_dotenv

voted = []
options = {}
HELP = "Here are the following usages of the poll bot \n _poll POLLNAME [option1] [option2] [...] \n " \
       "_display - displays a list of everyone who voted \n _update [option] [score] \n _vote [option] \n _help - displays this message"

load_dotenv(find_dotenv('token.env'))
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    voteResponse = False
    count = 0
    if message.author == client.user:
        return

    split = message.content.split()

    if split[0] == '_poll':
        options.clear()
        voted.clear()
        name = split[1]
        await message.channel.send(name + " created")
        for x in split:
            if count == 0 or count == 1:
                count += 1
                continue
            options.update({x:0})

    if split[0] == '_vote':
        if message.author in voted:
            await message.channel.send("You have already voted")
        else:
            option = split[1]
            for x, y in options.items():
                if x == option:
                    y += 1
                    options.update({option:y})
                    voteResponse = True
                    break

            if voteResponse:
                voted.append(message.author)
            for x, y in options.items():
                await message.channel.send(x + " " + str(y))

    if split[0] == '_help':
        await message.channel.send(HELP)

    if split[0] == '_score':
        for x, y in options.items():
            await message.channel.send(x + " " + str(y))

    if split[0] == '_update':
        name = split[1]
        number = split[2]
        options.update({name:number})
        for x, y in options.items():
            await message.channel.send(x + " " + str(y))

    if split[0] == '_display':
        await message.channel.send("Voters:")
        for x in voted:
            await message.channel.send(x)

client.run(TOKEN)