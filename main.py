
from random import Random
import traceback
import aiohttp
import asyncio
import os
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv,find_dotenv
from database import is_registered_user,clean_database,update_player_faction_rank,is_registered_rpg_user
from rank_verify import verify
from status import status_task
from roles import sfpd_roles,get_rank_role
import help_command,playerinfo_command,factions_command,leaders_command,helpers_command
from rank_watcher import watcher
from forum_tracker import tracker
from unit_functions import role_update_embed_generator,imagur_upload_embed_generator,channel_id,global_url,guild_id
from imgur_upload_handler import imgur_hanlder
from reminder import training_reminder
from bs4 import BeautifulSoup


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
    client.loop.create_task(training_reminder(client))
    client.loop.create_task(watcher(client,discord,asyncio))
    client.loop.create_task(tracker(client,discord))
#------------------------------- Utility Commands-Ends ----------------------------------

@client.event
async def on_message(message):
    if(message.channel.id in [channel_id["sfpd_imgur"],959138134413684840,990562699056402462]):
        images = message.attachments
        if(len(images)>0):
            info_message = await message.channel.send(embed=imagur_upload_embed_generator(discord,"Uploading your images","Please wait for a while"))
            await message.delete()
            imgur_result = await imgur_hanlder(images)
            await info_message.edit(embed=imagur_upload_embed_generator(discord,"Uploaded Successfully","Premanent link has been sent to you via DIRECT MESSAGE"))
            await message.author.send(embed = imagur_upload_embed_generator(discord,"Your Post","Hello there, Your images has been uploaded successfully",True,imgur_result))
            await asyncio.sleep(3)
            await info_message.delete()
        elif(message.author.id != 959137131605934113):
            await message.delete()
    else:
        await client.process_commands(message)

@client.event
async def on_member_join(member):
    print(member.guild.id)
    if member.guild.id in [guild_id["sfpd"]]:
        is_old_user = is_registered_user(member.id)
        print(bool(is_old_user))
        if(bool(is_old_user)):
            is_valid_faction_member={}
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://www.rpg.b-zone.ro/players/faction/{is_old_user["player_name"]}') as resp:
                    content = await resp.text()
                    doc = BeautifulSoup(content, "html.parser")
                    faction_name = (doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].a == None) and doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].string.strip() or doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].a.string.strip()
                    if(faction_name == "Civilian"):
                        is_valid_faction_member = {"is_civilian":1,"other_faction":1}
                    elif(faction_name == "SF School Instructors"):
                        is_valid_faction_member = {"other_faction":1}
                    elif(faction_name == "SFPD"):
                        is_valid_faction_member = {
                            "faction_name":"SFPD",
                            "faction_rank":doc.select("#FactionWrapper > table > tr:nth-child(3) > td:nth-child(2)")[0].string.strip(),
                            "faction_warn":doc.select("#FactionWrapper > table > tr:nth-child(4) > td:nth-child(2)")[0].string.strip(),
                            "other_faction":0
                        }
                    else:
                        is_valid_faction_member = {"other_faction":1}
                    print(is_valid_faction_member)


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
async def on_command_error(ctx,error = ""):
    def get_error_embed(error,message):
        if(error == "MissingRequiredArgument"):
            title = "Missing Required Argument"
            description = "Please enter all the required arugments"
        elif(error == "MissingPermissions"):
            title = "Missing Permissions"
            description = "Please update my permission and then use that command"
        elif(error == "MemberNotFound"):
            title = "Member Not Found"
            description = "Please mention the valid member (@mention)"
        elif(error == "CommandNotFound"):
            title = "Command Not Found"
            description = "Please use the valid command, use [!help] to know more"
        elif(error == "CommandInvokeError"):
            title = "Ops An Error Occured"
            description = "Please wait, there's some issue with backend server"
        elif(error == "CommandOnCooldown"):
            title = "Command On Cooldown"
            description = message
        embed = discord.Embed(
        title=f'**{title}**',
        description=description,
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
        return embed

    if isinstance(error,commands.MissingPermissions):
        await ctx.reply(embed = get_error_embed("MissingPermissions",error))

    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.reply(embed = get_error_embed("MissingRequiredArgument",error))
    
    elif isinstance(error,commands.MemberNotFound):
        await ctx.reply(embed = get_error_embed("MemberNotFound",error))

    elif isinstance(error,commands.CommandNotFound):
        print(error)
        await ctx.reply(embed = get_error_embed("CommandNotFound",error))

    elif isinstance(error,commands.CommandInvokeError):
        print(error)
        await ctx.reply(embed = get_error_embed("CommandInvokeError",error))
    
    elif isinstance(error,commands.CommandOnCooldown):
        print(error)
        await ctx.reply(embed = get_error_embed("CommandOnCooldown",error))

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
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
    await ctx.reply(embed = embed)





#------------------------------- Utility Commands-Ends ----------------------------------


#------------------------------- RPG Commands-Starts ----------------------------------


@client.command(aliases = ["pi","id"])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def playerinfo(ctx,player_name):
    start_time = time.time()
    try:
        embed = discord.Embed(
            description="**Fetching Your In-Game data** \n Please wait for a while",
            color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
        await ctx.reply(embed = embed)
        data={}
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.rpg.b-zone.ro/players/general/{player_name}') as resp:
                content = await resp.text()
                doc = BeautifulSoup(content, "html.parser")
                rpg_player_ign = doc.select(".tooltipstered a")
                print(len(rpg_player_ign))
                if(len(rpg_player_ign) != 0):
                    full_name =len(rpg_player_ign) > 1 and f'{rpg_player_ign[0].string}{rpg_player_ign[1].string}' or rpg_player_ign[0].string
                    print("player found")            
                    data = {
                            "ign": full_name,
                            "profile_url":f'https://www.rpg.b-zone.ro/players/general/{player_name}',
                            "avatar_url": doc.select(".skinImg")[0]["src"],
                            "current_status": doc.select("#wrapper > div.generalRight > table > tr.firstRow > td:nth-child(2) > div > div > div > div:nth-child(1) > img")[0]["alt"],
                            "level":doc.select("#generalTableLeft > table > tr:nth-child(3) > td:nth-child(2)")[0].string.strip(),
                            "last_login":doc.select("#wrapper > div.generalRight > table > tr:nth-child(3) > td:nth-child(2)")[0].string.strip(),
                            "hours_played_this_month":doc.select("#generalTableLeft > table > tr:nth-child(6) > td:nth-child(2)")[0].string.strip(),
                            "real_hours_this_month":doc.select("#generalTableLeft > table > tr:nth-child(7) > td:nth-child(2)")[0].string.strip(),
                            "respect":doc.select("#generalTableLeft > table > tr:nth-child(4) > td:nth-child(2)")[0].string.strip(),
                            "hours_played":doc.select("#generalTableLeft > table > tr:nth-child(5) > td:nth-child(2)")[0].string.strip(),
                            "forum_profile_link":(len(doc.select("#contentPage > div.subPageTitle.pageTitle > div > a")) == 1)and doc.select("#contentPage > div.subPageTitle.pageTitle > div > a")[0]["href"] or False,
                            "playerFound":1,
                            "message":0
     
                            }
                    async with session.get(f'https://www.rpg.b-zone.ro/players/faction/{player_name}') as resp:
                        content = await resp.text()
                        doc = BeautifulSoup(content, 'html.parser')
                        faction_name = (doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].a == None) and doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].string.strip() or doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].a.string.strip()
                        faction_data = {
                            "faction_name":faction_name,
                            "join_date": doc.select("#FactionWrapper > table > tr:nth-child(2) > td:nth-child(2)")[0].string.strip(),
                            "rank": doc.select("#FactionWrapper > table > tr:nth-child(3) > td:nth-child(2)")[0].string.strip(),
                            "faction_warns": doc.select("#FactionWrapper > table > tr:nth-child(4) > td:nth-child(2)")[0].string.strip(),
                            "faction_punish": doc.select("#FactionWrapper > table > tr:nth-child(5) > td:nth-child(2)")[0].string.strip(),
                            "faction_time": doc.select("#FactionWrapper > table > tr:nth-child(6) > td:nth-child(2)")[0].string.strip(),
                            "faction_url" : (faction_name != 'Civilian') and doc.select("#FactionWrapper > table > tr.firstRow > td:nth-child(2) > a")[0]["href"] or None,
                                }
                        data.update(faction_data)
                        if(faction_name != 'Civilian'):
                            async with session.get(f'https://www.rpg.b-zone.ro/{data["faction_url"]}') as resp:
                                content = await resp.text()
                                doc = BeautifulSoup(content, 'html.parser')
                                data.update({
                                    "faction_logo_url":doc.select("#pageContent > p:nth-child(3) > img")[0]["src"]
                                })
                        else:
                            print("Player is civilian")
                    end_time = time.time()
                    total_time = "Result in : {} seconds".format(int(end_time - start_time)) 
                    print(total_time)
                    await playerinfo_command.playerinfo_func(discord,ctx,data,total_time)
                else:
                    end_time = time.time()
                    total_time = "Result in : {} seconds".format(int(end_time - start_time)) 
                    print(total_time)
                    await playerinfo_command.playerinfo_func(discord,ctx,{"playerFound":0},total_time)

    except Exception:
        print(traceback.print_exc())
        embed = discord.Embed(
        title="**Error occured**",
        description="Please wait, there's some issue with backend server",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
        await ctx.reply(embed = embed)






@client.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
async def factions(ctx):
    embed = discord.Embed(
        description="**Fetching the factions details** \n Please wait for a while",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
    await ctx.reply(embed = embed)
    try:
        start_time = time.time()
        data = {}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.rpg.b-zone.ro/factions/index') as resp:
                    content = await resp.text()
                    doc = BeautifulSoup(content, "html.parser")

                    peaceful_factions = []
                    gang_factions = []
                    department_factions = []
                    mixt_faction = []
                    for i in range(2,9,2):
                        for j in range(3,12,1):
                            if(i == 2 and j < 12):
                                temp_name = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(1) > a > a')[0].string.strip()
                                temp_members = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(2)')[0].string.strip()
                                temp_faction_status = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(4)')[0].i.string.strip()
                                peaceful_factions.append({"name":temp_name,"members":temp_members,"status":temp_faction_status})
                            elif(i == 4 and j < 12):
                                temp_name = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(1) > a > a')[0].string.strip()
                                temp_members = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(2)')[0].string.strip()
                                temp_faction_status = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(4)')[0].i.string.strip()
                                gang_factions.append({"name":temp_name,"members":temp_members,"status":temp_faction_status})
                            elif(i ==6 and j < 8):
                                temp_name = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(1) > a > a')[0].string.strip()
                                temp_members = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(2)')[0].string.strip()
                                temp_faction_status = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(4)')[0].i.string.strip()
                                department_factions.append({"name":temp_name,"members":temp_members,"status":temp_faction_status})
                            elif(i == 8 and j<4):
                                temp_name = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(1) > a > a')[0].string.strip()
                                temp_members = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(2)')[0].string.strip()
                                temp_faction_status = doc.select(f'#contentPage > div:nth-child({i}) > table > tr:nth-child({j}) > td:nth-child(4)')[0].i.string.strip()
                                mixt_faction.append({"name":temp_name,"members":temp_members,"status":temp_faction_status})
                        
                    data = {
                        "Peaceful_faction":peaceful_factions,
                        "gang_factions":gang_factions,
                        "department_factions":department_factions,
                        "mixt_faction":mixt_faction
                    }
                    
                    end_time = time.time()
                    total_time = "Total execution time: {} seconds".format(int(end_time - start_time)) 
                    print(total_time)

                    await factions_command.factions(data,discord,ctx,total_time)

    except:
        embed = discord.Embed(
        title="**Error occured**",
        description="Please wait, there's some issue with backend server",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
        await ctx.reply(embed = embed)



@client.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
async def leaders(ctx):
    embed = discord.Embed(
        description="**Fetching the leaders details** \n Please wait for a while",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
    await ctx.reply(embed = embed)
    try:
        start_time = time.time()
        data = {}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.rpg.b-zone.ro/staff/leaders') as resp:
                    content = await resp.text()
                    doc = BeautifulSoup(content, "html.parser")
                    peaceful_factions_leaders = []
                    gang_factions_leaders = []
                    department_factions_leaders = []
                    for j in range(6,11,2):
                            for i in range(2,11,1):
                                    if(j==6 and i < 11):
                                            temp_name = (len(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')) > 1) and "{}{} | [{}]".format(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string.strip(),doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[1].string.strip(),doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(1) > img')[0]["alt"]) or "".format(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string.strip(),doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(1) > img')[0]["alt"])
                                            temp_faction_name = doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(4)')[0].string
                                            temp_last_login = doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(6)')[0].string
                                            peaceful_factions_leaders.append({"name":temp_name,"faction":temp_faction_name,"last_login":temp_last_login})
                                    elif(j==8 and i<11):
                                            temp_name = (len(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')) > 1) and "{}{} | [{}]".format(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string.strip(),doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[1].string.strip(),doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(1) > img')[0]["alt"]) or "".format(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string.strip(),doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(1) > img')[0]["alt"])
                                            temp_faction_name = doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(4)')[0].string
                                            temp_last_login = doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(6)')[0].string
                                            gang_factions_leaders.append({"name":temp_name,"faction":temp_faction_name,"last_login":temp_last_login})
                                    elif(j==10 and i<7 ):
                                            temp_name = (len(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')) > 1) and "{}{} | [{}]".format(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string.strip(),doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[1].string.strip(),doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(1) > img')[0]["alt"]) or "".format(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string.strip(),doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(1) > img')[0]["alt"])
                                            temp_faction_name = doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(4)')[0].string
                                            temp_last_login = doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(6)')[0].string
                                            department_factions_leaders.append({"name":temp_name,"faction":temp_faction_name,"last_login":temp_last_login})
                    data = {
                    "Peaceful_faction":peaceful_factions_leaders,
                    "gang_factions":gang_factions_leaders,
                    "department_factions":department_factions_leaders,
                    }    
                    end_time = time.time()
                    total_time = "Total execution time: {} seconds".format(int(end_time - start_time)) 
                    print(total_time)
                    await leaders_command.leaders(data,discord,ctx,total_time)

    except:
        embed = discord.Embed(
        title="**Error occured**",
        description="Please wait, there's some issue with backend server",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
        await ctx.reply(embed = embed)


@client.command(aliases = ["admins"])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def helpers(ctx):
    embed = discord.Embed(
        description="**Fetching Staffs details** \n Please wait for a while",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
    await ctx.reply(embed = embed)
    try:
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.rpg.b-zone.ro/staff/helpers') as resp:
                content = await resp.text()
                doc = BeautifulSoup(content, "html.parser")
                level_1_helpers = []
                level_2_helpers = []
                level_3_helpers = []
                for j in range(5,8):
                    total_number_of_helpers = len(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr')) + 1
                    for i in range(2,total_number_of_helpers):    
                        if(j==5 and i<total_number_of_helpers):
                            temp_name = len(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')) > 1 and "{}{}".format( doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string,doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[1].string) or doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string
                            temp_status =  doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(1) > img')[0]["alt"]
                            temp_last_login =  doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(4)')[0].string.strip()
                            level_3_helpers.append({"name":temp_name,"current_status":temp_status,"last_login":temp_last_login})
                        elif(j==6 and i<total_number_of_helpers):
                            temp_name = len(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')) > 1 and "{}{}".format( doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string,doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[1].string) or doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string
                            temp_status =  doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(1) > img')[0]["alt"]
                            temp_last_login =  doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(4)')[0].string.strip()
                            level_2_helpers.append({"name":temp_name,"current_status":temp_status,"last_login":temp_last_login})
                        elif(j==7 and i<total_number_of_helpers ):
                            temp_name = len(doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')) > 1 and "{}{}".format( doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string,doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[1].string) or doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(2) > a')[0].string
                            temp_status =  doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(1) > div > div:nth-child(1) > img')[0]["alt"]
                            temp_last_login =  doc.select(f'#contentPage > div > div:nth-child({j}) > table > tr:nth-child({i}) > td:nth-child(4)')[0].string.strip()
                            level_1_helpers.append({"name":temp_name,"current_status":temp_status,"last_login":temp_last_login})
        
        
                data ={
                    "level_1_helpers":level_1_helpers,
                    "level_2_helpers":level_2_helpers,
                    "level_3_helpers":level_3_helpers,
                }
                end_time = time.time()
                total_time = "Total execution time: {} seconds".format(int(end_time - start_time)) 
                print(total_time)
                await helpers_command.helpers(data,discord,ctx,total_time)

    except:
        embed = discord.Embed(
        title="**Error occured**",
        description="Please wait, there's some issue with backend server",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
        await ctx.reply(embed = embed)



@client.command(aliases = ["sv"])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def sverify(ctx,player_name):
    channels_id = [channel_id["sfpd_verification_channel"]] 
    if(ctx.channel.id in channels_id):
        is_already_registered_user = is_registered_user(ctx.message.author.id)
        if(bool(is_already_registered_user) and is_already_registered_user["player_discord_id"] == ctx.message.author.id):
            embed = discord.Embed(
                title="[⛔] Something went wrong",
                description="**It seems your Discord Account is already resigtered with another one RPG Account ** \n Please contact Dabrovsky if you like to make changes ",
                color=discord.Colour.random()
            )
            embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
            await ctx.reply(embed = embed)
        else:
            is_already_registered_rpg_username = is_registered_rpg_user(player_name)
            print(is_already_registered_rpg_username)
            if(bool(is_already_registered_rpg_username)):
                embed = discord.Embed(
                    title="[⛔] Something went wrong",
                    description="**It seems your RPG Account is already resigtered with another one discord id ** \n Please contact Dabrovsky if you like to make changes ",
                    color=discord.Colour.random()
                )
                embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
                await ctx.reply(embed = embed)
            else:
                if(ctx.channel.id in channels_id):
                    try:
                        embed = discord.Embed(
                            description="**Fetching Your In-Game data** \n Please wait for a while",
                            color=discord.Colour.random()
                        )
                        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
                        await ctx.reply(embed = embed)
                        data={}
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f'https://www.rpg.b-zone.ro/players/faction/{player_name}') as resp:
                                content = await resp.text()
                                doc = BeautifulSoup(content, "html.parser")
                                if(len(doc.select("#contentPage > div")[0])>1):
                                    faction_name = (doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].a == None) and doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].string.strip() or doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].a.string.strip()
                                    if(faction_name == "Civilian"):
                                        data = {"is_civilian":1,"other_faction":1}
                                    elif(faction_name == "SF School Instructors"):
                                        data = {"other_faction":1}
                                    elif(faction_name == "SFPD"):
                                        data = {
                                            "faction_name":"SFPD",
                                            "faction_rank":doc.select("#FactionWrapper > table > tr:nth-child(3) > td:nth-child(2)")[0].string.strip(),
                                            "faction_warn":doc.select("#FactionWrapper > table > tr:nth-child(4) > td:nth-child(2)")[0].string.strip(),
                                            "other_faction":0
                                        }
                                    else:
                                        data = {"other_faction":1}
                                    print(data)
                                    await verify(discord,ctx,data,player_name)
                                elif(len(doc.select("#contentPage > div")[0]) == 1):
                                    embed = discord.Embed(
                                    title="**Player Not Found**",
                                    description="Player not found, Please enter the valid name",
                                    color=discord.Colour.random()
                                    )
                                    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
                                    await ctx.reply(embed = embed)
                    except :
                        embed = discord.Embed(
                        title="**Error occured**",
                        description="Please wait, there's some issue with backend server",
                        color=discord.Colour.random()
                        )
                        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
                        await ctx.reply(embed = embed)
    else:
        embed = discord.Embed(
        title="[⛔] WARNING",
        description="**This command only works on SFPD server's #verification channel**",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
        await ctx.reply(embed = embed)




@client.command()
@commands.cooldown(1, 600, commands.BucketType.guild)
async def suggestions(ctx,*,message):
    channel = client.get_channel(channel_id["sfpd_suggestion_channel_id"])
    embed = discord.Embed(
        title=f'Suggestion from {ctx.author} | [server : {ctx.guild}]',
        description=f'[Message] : **{message}**',
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
    await channel.send(embed = embed)
    
    embed = discord.Embed(
        title="Successfully sent 👍",
        description="Thanks for sharing your priceless suggestion / report 💖",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
    reply_message = await ctx.reply(embed = embed)
    await asyncio.sleep(4)
    await ctx.message.delete()
    await reply_message.delete()




@client.command()
async def forum(ctx):
    embed = discord.Embed(
        title="[📕] SF Police Department Forum",
        description="Serving with pride, Protecting with honor!",
        color=discord.Colour.random()
    )
    embed.add_field(name="Topics",value=">>> [[ 📣 ] Important Announcements](https://forum.b-zone.ro/topic/123508-sf-police-department-%F0%9F%93%A3-anun%C5%A3uri-importante-important-announcements-%F0%9F%93%A3/)\n[[ 🎯 ] Challenge of the week](https://forum.b-zone.ro/topic/356270-sf-police-departament-misiunea-s%C4%83pt%C4%83m%C3%A2nii-challenge-of-the-week/)\n[[ 📌 ] Internal Rules ](https://forum.b-zone.ro/topic/422237-sf-police-department-%F0%9F%93%8C-regulament-intern-internal-rules-%F0%9F%93%8C/)\n[[ 🔖 ]Wanted, Arrest and Ticket List](https://forum.b-zone.ro/topic/122599-sf-police-department-wanted-arrest-and-ticket-list/)\n[[ 🎫 ] Training Pass Requests ](https://forum.b-zone.ro/topic/384352-sf-police-department-%F0%9F%9F%A2-%C3%AEnvoiri-pass-requests-%F0%9F%9F%A2/)\n[[ 👮‍♂️ ] Officers of the week ](https://forum.b-zone.ro/topic/430679-sf-police-department-ofi%C8%9Berii-s%C4%83pt%C4%83m%C3%A2nii-officers-of-the-week/)\n")
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
    await ctx.reply(embed=embed)



@client.command()
async def fmotd(ctx,*,message):
    if(ctx.author.id in [491251010656927746,339956284205826048,374223751669088256]):
        embed = discord.Embed(
            title = f'Fmotd announcement',
            description=f"_{message}_",
            color= discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
        channel = client.get_channel(channel_id["sfpd_announcement"])
        await channel.send(f'<@&{sfpd_roles["verified"]}>',embed = embed)
    else:
        embed = discord.Embed(
        title="[⛔] WARNING",
        description="**You are not allowed to use this command**",
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
        warn_msg = await ctx.reply(embed = embed)
        await asyncio.sleep(5)
        await warn_msg.delete()




#---------------------------- RPG Commands-Ends ----------------------------------

#------------------------------- Help Commands-Starts ----------------------------------


@client.command(aliases = ["h"])
async def help(ctx):
    await help_command.help(discord,client,ctx)
 

#------------------------------- Help Commands-Ends ----------------------------------


#------------------------------- Experiment Commands-starts ----------------------------------


#------------------------------- Experiment Commands-ends ----------------------------------










client.run(os.environ.get("TOKEN"))






