
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
from unit_functions import role_update_embed_generator,imagur_upload_embed_generator,channel_id,global_url
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
    if(message.channel.id in [channel_id["sfpd_imgur"],959138134413684840]):
        images = message.attachments
        if(len(images)>0):
            info_message = await message.channel.send(embed=imagur_upload_embed_generator(discord,"Uploading your images","Please wait for a while"))
            
            imgur_result = {}

            API_ENDPOINT = "https://api.imgur.com/3"
            headers = {
                "Authorization":f'Client-ID {os.environ.get("CLIENT_ID")}'
            }
            data = {
                "privacy":"hidden"
            }    
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url = f'{API_ENDPOINT}/album', data = data,headers=headers) as resp:
                    res = await resp.json()
                    album_id = res["data"]["id"]
                    album_delete_hash_id = res["data"]["deletehash"]

                    uploaded_images_id = []
                    uploaded_images_deletehash_id = []
                    uploaded_images_link = []
                    for image in images:
                        image_post_data = {
                            "image":image.url,
                            "type":"url",
                        }
                        async with aiohttp.ClientSession() as session:
                            async with session.post(url= f'{API_ENDPOINT}/upload',data=image_post_data,headers=headers) as resp:
                                res = await resp.json()
                                uploaded_images_link.append(res["data"]["link"])
                                uploaded_images_id.append(res["data"]["id"])
                                uploaded_images_deletehash_id.append(res["data"]["deletehash"])

                                #https://api.imgur.com/3/
                                album_image_add_data = {
                                    "deletehashes[]":uploaded_images_deletehash_id
                                }
                                async with aiohttp.ClientSession() as session:
                                    async with session.post(url= f'{API_ENDPOINT}/album/{album_delete_hash_id}/add',data=album_image_add_data,headers=headers) as resp:
                                        res = await resp.json()
                                        
                                        #https://api.imgur.com/3/album/{{albumHash}}
                                        async with aiohttp.ClientSession() as session:
                                            async with session.get(url= f'{API_ENDPOINT}/album/{album_id}',headers=headers) as resp:
                                                res = await resp.json()
                                                print("\n Album links \n")
                                                album_link = {
                                                    "first_image_link":uploaded_images_link[0],
                                                    "album_post_link":res["data"]["link"]
                                                    }

                                                print(album_link)
                                                imgur_result = album_link
            
            
            
            # imgur_result = await imgur_hanlder(images)
            await info_message.edit(embed=imagur_upload_embed_generator(discord,"Uploaded Successfully","Premanent link has been sent to you via DIRECT MESSAGE"))
            await message.author.send(embed = imagur_upload_embed_generator(discord,"Your Post","Hello there, Your images has been uploaded successfully",True,imgur_result))
            await asyncio.sleep(3)
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
                    #  return{
                    #      faction_name:"SF School Instructors",
                    #      faction_rank:doc.select("#FactionWrapper > table > tr:nth-child(3) > td:nth-child(2)")[0].string.strip(),
                    #      faction_warn:doc.select("#FactionWrapper > table > tr:nth-child(4) > td:nth-child(2)")[0].string.strip(),
                    #      other_faction:0
                    #  }
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
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
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
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
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
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
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
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        await ctx.reply(embed = embed)






@client.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
async def factions(ctx):
    embed = discord.Embed(
        description="**Fetching the factions details** \n Please wait for a while",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    await ctx.reply(embed = embed)
    try:
            time.sleep(8)
            async with aiohttp.ClientSession() as session:
                site_url = f'{global_url}/factions'
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
@commands.cooldown(1, 5, commands.BucketType.guild)
async def leaders(ctx):
    embed = discord.Embed(
        description="**Fetching the leaders details** \n Please wait for a while",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    await ctx.reply(embed = embed)
    try:
            time.sleep(8)
            async with aiohttp.ClientSession() as session:
                site_url = f'{global_url}/leaders'
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
@commands.cooldown(1, 5, commands.BucketType.guild)
async def helpers(ctx):
    embed = discord.Embed(
        description="**Fetching Staffs details** \n Please wait for a while",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    await ctx.reply(embed = embed)
    try:
            time.sleep(8)
            async with aiohttp.ClientSession() as session:
                site_url = f'{global_url}/helpers'
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
@commands.cooldown(1, 5, commands.BucketType.guild)
async def sverify(ctx,player_name):
    channels_id = [channel_id["sfpd_verification_channel"]] 
    is_already_registered_user = is_registered_user(ctx.message.author.id)
    if(bool(is_already_registered_user) and is_already_registered_user["player_discord_id"] == ctx.message.author.id):
        embed = discord.Embed(
            title="Oops, Something went wrong",
            description="**It seems your Discord Account is already resigtered with another one RPG Account ** \n Please contact Dabrovsky if you like to make changes ",
            color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        await ctx.reply(embed = embed)
    else:
        is_already_registered_rpg_username = is_registered_rpg_user(player_name)
        print(is_already_registered_rpg_username)
        if(bool(is_already_registered_rpg_username)):
            embed = discord.Embed(
                title="Oops, Something went wrong",
                description="**It seems your RPG Account is already resigtered with another one discord id ** \n Please contact Dabrovsky if you like to make changes ",
                color=discord.Colour.random()
            )
            embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
            await ctx.reply(embed = embed)
        else:
            if(ctx.channel.id in channels_id):
                try:
                    embed = discord.Embed(
                        description="**Fetching Your In-Game data** \n Please wait for a while",
                        color=discord.Colour.random()
                    )
                    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
                    await ctx.reply(embed = embed)
                    data={}
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f'https://www.rpg.b-zone.ro/players/faction/{player_name}') as resp:
                            content = await resp.text()
                            doc = BeautifulSoup(content, "html.parser")
                            faction_name = (doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].a == None) and doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].string.strip() or doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].a.string.strip()
                            if(faction_name == "Civilian"):
                                data = {"is_civilian":1,"other_faction":1}
                            elif(faction_name == "SF School Instructors"):
                                data = {"other_faction":1}
                                #  return{
                                #      faction_name:"SF School Instructors",
                                #      faction_rank:doc.select("#FactionWrapper > table > tr:nth-child(3) > td:nth-child(2)")[0].string.strip(),
                                #      faction_warn:doc.select("#FactionWrapper > table > tr:nth-child(4) > td:nth-child(2)")[0].string.strip(),
                                #      other_faction:0
                                #  }
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
                except :
                    embed = discord.Embed(
                    title="**Error occured**",
                    description="Please wait, there's some issue with backend server",
                    color=discord.Colour.random()
                    )
                    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
                    await ctx.reply(embed = embed)
        




@client.command()
@commands.cooldown(1, 600, commands.BucketType.guild)
async def suggestions(ctx,*,message):
    channel = client.get_channel(channel_id["sfpd_suggestion_channel_id"])
    embed = discord.Embed(
        title=f'Suggestion from {ctx.author}',
        description=f'[Message] : **{message}**',
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    await channel.send(embed = embed)
    
    embed = discord.Embed(
        title="Successfully sent 👍",
        description="Thanks for sharing your priceless suggestion / report 💖",
        color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
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
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    await ctx.reply(embed=embed)


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


#------------------------------- Experiment Commands-starts ----------------------------------

#------------------------------- Experiment Commands-ends ----------------------------------
























client.run(os.environ.get("TOKEN"))






