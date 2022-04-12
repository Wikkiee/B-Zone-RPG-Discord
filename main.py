import aiohttp
import asyncio
import os
import time
import discord
from discord.ext import commands
from discord.ui import Button,View
from dotenv import load_dotenv,find_dotenv

from modules import dm_message,help_command,playerinfo_command,status

load_dotenv(find_dotenv())

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!",intents = intents)
client.remove_command("help")

@client.event
async def on_ready():
    print("Our bot successfully logged in as {0.user}".format(client))
    client.loop.create_task(status.status_task(client,asyncio,discord))


@client.event
async def on_message(message):
        await dm_message.dm_messages(client,message)



@client.command(aliases = ["pi"])
async def playerinfo(ctx,player_name):
    try:
        embed = discord.Embed(
        description="**Fetching Your In-Game data** \n Please wait for a while",
        color=discord.Colour.random()
    )
        await ctx.reply(embed = embed)
        data={}
        try:
            time.sleep(5)
            async with aiohttp.ClientSession() as session:
                site_url = 'https://bzone-bot-api.herokuapp.com/playerinfo/{}'.format(player_name)
                #site_url = 'http://localhost:3000/playerinfo/{}'.format(player_name)
                print("\n \nSite URL : " + site_url + "\n \n")
                async with session.get(site_url) as resp:
                    data = await resp.json()
                    print(data)
                    await playerinfo_command.playerinfo_func(discord,ctx,data)

        except None:
            print("error")
    except:
        embed = discord.Embed(
        description="**Error** \n Please enter a valid user name",
        color=discord.Colour.random()
    )
        await ctx.reply(embed = embed)




@client.command(aliases = ["sp"])
async def spamcommand(ctx,limit,*,msg):
    button = Button(label="Click me",style=discord.ButtonStyle.primary)
    view = View()
    view.add_item(button)
    try:
        if ctx.author.id == 491251010656927746:
            for i in range(1,int(limit)+1):
                print("User name : {} \nUser ID : {}".format(ctx.author,ctx.author.id))
                await ctx.send(msg,view=view)
        elif ctx.author.id == 664492070336987168:
            for i in range(1,int(limit)+1):
                print("User name : {} \nUser ID : {}".format(ctx.author,ctx.author.id))
                await ctx.send(msg,view=view)
        else:
            print("User name : {} \n User ID : {}".format(ctx.author,ctx.author.id))
            await ctx.reply("You are not authorized to use this command...")
    except:
        ctx.reply("Error")
            

@client.command(aliases = ["h"])
async def help(ctx):
    await help_command.help(discord,client,ctx)
 



client.run(os.environ.get("TOKEN"))










#@client.command(aliases = ["termi"] )
# async def terminate(ctx, password):
#     print
#     if int(password) == 123:
#         await ctx.reply("Terminating...")
#         await client.close()
#     else:
#         await ctx.reply("please enter the valid password")
