import aiohttp
import asyncio
import os
import time
import discord
from discord.ext import commands
from discord.ui import Button,View
from dotenv import load_dotenv,find_dotenv

import dm_message,help_command,playerinfo_command,status,factions_command,leaders_command,helpers_command

load_dotenv(find_dotenv())

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!",intents = intents)
client.remove_command("help")

@client.event
async def on_ready():
    print("Our bot successfully logged in as {0.user}".format(client))
    client.loop.create_task(status.status_task(client,asyncio,discord))


#------------------------------- Utility Commands-Ends ----------------------------------

@client.event
async def on_message(message):
        await dm_message.dm_messages(client,message)

@client.event
async def on_command_error(ctx,error):

    if isinstance(error,commands.MissingPermissions):
        print("Working")
    elif isinstance(error,commands.MissingRequiredArgument):
        embed = discord.Embed(
        title="**Error occured**",
        description="Please enter all the required arugments",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
   
        await ctx.reply(embed = embed)
    elif isinstance(error,commands.MemberNotFound):
        embed = discord.Embed(
        title="**Error occured**",
        description="Please mention the valid member (@mention)",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
   
        await ctx.reply(embed = embed)
    elif isinstance(error,commands.CommandNotFound):
        embed = discord.Embed(
        title="**Error occured**",
        description="Please use the valid command, use [!help] to know more",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        await ctx.reply(embed = embed)
    
    else:
        raise error


@client.command()
async def pfp(ctx,user:discord.Member):
    link = str(user.display_avatar)
    embed = discord.Embed(
        title="Download the picture",
        description="[128]({}) | [256]({}) | [512]({}) | [1024]({})".format(""+link[:-4]+"128",""+link[:-4]+"256",""+link[:-4]+"512",""+link[:-4]+"1024"),
        color=discord.Colour.random(),
    )
    embed.set_image(url=link)
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
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
            

#------------------------------- Utility Commands-Ends ----------------------------------


#------------------------------- RPG Commands-Starts ----------------------------------


@client.command(aliases = ["pi","id"])
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
                #site_url = 'https://bzone-bot-api.herokuapp.com/playerinfo/{}'.format(player_name)
                site_url = 'http://localhost:3000/playerinfo/{}'.format(player_name)
                async with session.get(site_url) as resp:
                    data = await resp.json()
                    await playerinfo_command.playerinfo_func(discord,ctx,data)

        except None:
            print("error")
    except:
        embed = discord.Embed(
        description="**Error** \n Please enter a valid user name",
        color=discord.Colour.random()
    )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        await ctx.reply(embed = embed)







@client.command()
async def factions(ctx):
    embed = discord.Embed(
        description="**Fetching the factions details** \n Please wait for a while",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    await ctx.reply(embed = embed)
    try:
            time.sleep(5)
            async with aiohttp.ClientSession() as session:
                site_url = 'http://localhost:3000/factions'
                async with session.get(site_url) as resp:
                    data = await resp.json()
                    await factions_command.factions(data,discord,ctx)

    except None:
            print("error")



@client.command()
async def leaders(ctx):
    embed = discord.Embed(
        description="**Fetching the leaders details** \n Please wait for a while",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    await ctx.reply(embed = embed)
    try:
            time.sleep(5)
            async with aiohttp.ClientSession() as session:
                site_url = 'http://localhost:3000/leaders'
                async with session.get(site_url) as resp:
                    data = await resp.json()
                    await leaders_command.leaders(data,discord,ctx)

    except None:
            print("error")


@client.command(aliases = ["admins"])
async def helpers(ctx):
    embed = discord.Embed(
        description="**Fetching Staffs details** \n Please wait for a while",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    await ctx.reply(embed = embed)
    try:
            time.sleep(5)
            async with aiohttp.ClientSession() as session:
                site_url = 'http://localhost:3000/helpers'
                async with session.get(site_url) as resp:
                    data = await resp.json()
                    await helpers_command.helpers(data,discord,ctx)

    except None:
            print("error")


#------------------------------- RPG Commands-Ends ----------------------------------

#------------------------------- Help Commands-Starts ----------------------------------


@client.command(aliases = ["h"])
async def help(ctx):
    await help_command.help(discord,client,ctx)
 

#------------------------------- Help Commands-Ends ----------------------------------


client.run(os.environ.get("TOKEN"))










#@client.command(aliases = ["termi"] )
# async def terminate(ctx, password):
#     print
#     if int(password) == 123:
#         await ctx.reply("Terminating...")
#         await client.close()
#     else:
#         await ctx.reply("please enter the valid password")
