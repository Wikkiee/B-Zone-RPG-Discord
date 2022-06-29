from distutils.log import info
from pyexpat.errors import messages
import aiohttp
import asyncio
import os
import time
import discord
from discord.ext import commands
from discord.ui import Button,View
from dotenv import load_dotenv,find_dotenv
from discord.ext.commands import has_permissions, CheckFailure
from database import insert_users_data,is_registered_user,clean_database,get_players_data,update_player_faction_rank
from sfsi_and_sfpd_manager_command import verify
from status import status_task
from roles import sfpd_roles,get_rank_role
import dm_message,help_command,playerinfo_command,factions_command,leaders_command,helpers_command
from rank_watcher import watcher
from forum_tracker import tracker
from unit_functions import role_update_embed_generator,imagur_upload_embed_generator
from imgur_upload_handler import imgur_hanlder

load_dotenv(find_dotenv())

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="!",intents = intents)
client.remove_command("help")

@client.event
async def on_ready():
    print("Discord Bot has logged in as {0.user}".format(client))
    client.loop.create_task(status_task(client,asyncio,discord))
    #client.loop.create_task(watcher(client,asyncio))

#------------------------------- Utility Commands-Ends ----------------------------------

@client.event
async def on_message(message):
    print(message)
    if(message.channel.id in [990562699056402462,991655147442802737]):
        images = message.attachments
        if(len(images)>0):
            await message.delete()
            info_message = await message.channel.send(embed=imagur_upload_embed_generator(discord,"Uploading your images","Please wait for a while"))
            imgur_result = await imgur_hanlder(images)
            await info_message.edit(embed=imagur_upload_embed_generator(discord,"Uploaded Successfully","Premanent link has been sent to you via DIRECT MESSAGE"))
            await asyncio.sleep(3)
            await message.author.send(embed = imagur_upload_embed_generator(discord,"Your Post","Hello there, Your images has been uploaded successfully",True,imgur_result))
            await info_message.delete()
        else:
            pass
    else:
        await client.process_commands(message)

@client.event
async def on_member_join(member):

    is_old_user = is_registered_user(member.id)
    print(bool(is_old_user))
    if(bool(is_old_user)):
        async with aiohttp.ClientSession() as session:
            #site_url = 'https://bzone-bot-api.herokuapp.com/playerinfo/{}'.format(player_name)
            #site_url= "https://bzone-bot-api-2.herokuapp.com/verify/{}".format(player_name)
            site_url = 'http://localhost:3000/verify/{}'.format(is_old_user["player_name"])
            async with session.get(site_url) as resp:
                is_valid_faction_member =  await resp.json()

                if(is_valid_faction_member["other_faction"]!=1):
                    if(is_valid_faction_member["faction_name"] == is_old_user["faction_name"]):
                        if(is_valid_faction_member["faction_rank"]== is_old_user["faction_rank"]):
                            role = member.guild.get_role(sfpd_roles["verified"])
                            await member.add_roles(role)
                            role = member.guild.get_role(get_rank_role(is_valid_faction_member["faction_name"],is_valid_faction_member["faction_rank"]))
                            await member.add_roles(role)
                            await member.edit(nick=is_old_user["player_name"])
                            await member.send(embed = role_update_embed_generator(discord,is_old_user["player_name"],is_valid_faction_member["faction_name"],is_valid_faction_member["faction_rank"]))
                        elif(is_valid_faction_member["faction_rank"] in ["Officer (1)","Detective (2)","Sergeant (3)","Lieutenant (4)","Captain (5)","Captain (5)","Assistant Chief (6)","Chief (Leader)"]):
                                print("Re-joined the faction")
                                faction_rank_update_result = update_player_faction_rank(is_old_user["player_discord_id"],is_valid_faction_member["faction_rank"])
                                if(faction_rank_update_result):
                                    role = member.guild.get_role(sfpd_roles["verified"])
                                    await member.add_roles(role)
                                    role = member.guild.get_role(get_rank_role(is_valid_faction_member["faction_name"],is_valid_faction_member["faction_rank"]))
                                    await member.add_roles(role)
                                    await member.edit(nick=is_old_user["player_name"])
                                    await member.send(embed = role_update_embed_generator(discord,is_old_user["player_name"],is_valid_faction_member["faction_name"],is_valid_faction_member["faction_rank"]))
                                else:
                                    print("Something wrong with DB")
                elif(is_valid_faction_member["other_faction"]==1):
                    if(is_old_user["faction_rank"] in ["Officer (1)","Detective (2)","Sergeant (3)","Lieutenant (4)","Captain (5)","Captain (5)","Assistant Chief (6)","Chief (Leader)"]):
                            faction_rank_update_result = update_player_faction_rank(is_old_user["player_discord_id"],"ex_member")
                            if(faction_rank_update_result):
                                role = member.guild.get_role(sfpd_roles["ex_member"])
                                await member.add_roles(role)
                                await member.edit(nick=is_old_user["player_name"])
                                await member.send(embed = role_update_embed_generator(discord,is_old_user["player_name"],is_old_user["faction_name"],"Ex-Member"))
                            else:
                                print("Something wrong with DB")
                    elif(is_old_user["faction_rank"] == "ex_member"):
                        role = member.guild.get_role(sfpd_roles["ex_member"])
                        await member.add_roles(role)
                        await member.edit(nick=is_old_user["player_name"])
                        await member.send(embed = role_update_embed_generator(discord,is_old_user["player_name"],is_old_user["faction_name"],"Ex-Member"))
                    else:
                        role = member.guild.get_role(sfpd_roles["other_faction_members"])
                        await member.add_roles(role)
                        await member.edit(nick=is_old_user["player_name"])
                        await member.send(embed = role_update_embed_generator(discord,is_old_user["player_name"],"Other","Other Faction Member"))
    else:   
        role = member.guild.get_role(sfpd_roles["unverified"])
        await member.add_roles(role)


@client.event
async def on_command_errors(ctx,error):

    def get_error_embed(error):
        if(error == "MissingRequiredArgument"):
            description = "Please enter all the required arugments"
        elif(error == "MissingPermissions"):
            description = "Please update my permission and then use that command"
        elif(error == "MemberNotFound"):
            description = "Please mention the valid member (@mention)"
        elif(error == "CommandNotFound"):
            description = "Please use the valid command, use [!help] to know more"
        elif(error == "CommandInvokeError"):
            description = "Please wait, there's some issue with backend server"
        embed = discord.Embed(
        title="**Error occured**",
        description=description,
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        return embed

    if isinstance(error,commands.MissingPermissions):
        await ctx.reply(embed = get_error_embed("MissingPermissions"))

    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.reply(embed = get_error_embed("MissingRequiredArgument"))
    
    elif isinstance(error,commands.MemberNotFound):
        await ctx.reply(embed = get_error_embed("MemberNotFound"))

    elif isinstance(error,commands.CommandNotFound):
        await ctx.reply(embed = get_error_embed("CommandNotFound"))

    # elif isinstance(error,commands.CommandInvokeError):
    #     await ctx.reply(embed = get_error_embed("MissingPermissions"))

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
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        await ctx.reply(embed = embed)
        data={}
        time.sleep(5)
        async with aiohttp.ClientSession() as session:
            #site_url = 'https://bzone-bot-api.herokuapp.com/playerinfo/{}'.format(player_name)
            site_url= "https://bzone-bot-api-2.herokuapp.com/playerinfo/{}".format(player_name)
            #site_url = 'http://localhost:3000/playerinfo/{}'.format(player_name)
            async with session.get(site_url) as resp:
                data = await resp.json()
                await playerinfo_command.playerinfo_func(discord,ctx,data)
    except:
        embed = discord.Embed(
        title="**Error occured**",
        description="Please wait, there's some issue with backend server",
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
                site_url= "https://bzone-bot-api-2.herokuapp.com/factions"
                #site_url = 'http://localhost:3000/factions'
                async with session.get(site_url) as resp:
                    data = await resp.json()
                    await factions_command.factions(data,discord,ctx)

    except:
        embed = discord.Embed(
        title="**Error occured**",
        description="Please wait, there's some issue with backend server",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        await ctx.reply(embed = embed)



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
                site_url= "https://bzone-bot-api-2.herokuapp.com/leaders"
                #site_url = 'http://localhost:3000/leaders'
                async with session.get(site_url) as resp:
                    data = await resp.json()
                    await leaders_command.leaders(data,discord,ctx)

    except:
        embed = discord.Embed(
        title="**Error occured**",
        description="Please wait, there's some issue with backend server",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        await ctx.reply(embed = embed)


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
                site_url= "https://bzone-bot-api-2.herokuapp.com/helpers"
                #site_url = 'http://localhost:3000/helpers'
                async with session.get(site_url) as resp:
                    data = await resp.json()
                    await helpers_command.helpers(data,discord,ctx)

    except:
        embed = discord.Embed(
        title="**Error occured**",
        description="Please wait, there's some issue with backend server",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        await ctx.reply(embed = embed)





@client.command(aliases = ["sv"])
async def sverify(ctx,player_name):
    channel_id = [990242620687122462,990485622403788841] 
    #print(ctx.channel.id)
    if(bool(is_registered_user(ctx.message.author.id))):
        embed = discord.Embed(
            title="Oops, Something went wrong",
            description="**It seems your RPG Account is already resigtered with another one discord id ** \n Please contact Dabrovsky if you like to make changes ",
            color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        await ctx.reply(embed = embed)
    else:
        if(ctx.channel.id in channel_id):
            try:

                embed = discord.Embed(
                    description="**Fetching Your In-Game data** \n Please wait for a while",
                    color=discord.Colour.random()
                )
                embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
                await ctx.reply(embed = embed)
                data={}
                time.sleep(3)
                async with aiohttp.ClientSession() as session:
                    #site_url = 'https://bzone-bot-api.herokuapp.com/playerinfo/{}'.format(player_name)
                    #site_url= "https://bzone-bot-api-2.herokuapp.com/verify/{}".format(player_name)
                    site_url = 'http://localhost:3000/verify/{}'.format(player_name)
                    async with session.get(site_url) as resp:
                        data = await resp.json()
                        await verify(discord,ctx,data,player_name)
            except :
                embed = discord.Embed(
                title="**Error occured**",
                description="Please wait, there's some issue with backend server",
                color=discord.Colour.random()
                )
                embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
                await ctx.reply(embed = embed)



@client.command()
async def t(ctx):
    await ctx.reply("Hi")
    await imgur_hanlder()




@client.command()
async def cdb(ctx):
    clean_database()
    await ctx.message.delete()

#---------------------------- RPG Commands-Ends ----------------------------------

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



