import aiohttp
from database import get_players_data,update_player_faction_rank,update_player_faction_name,update_player_other_faction
from roles import get_rank_role,sfpd_roles
from unit_functions import remove_role_function,role_update_embed_generator,channel_id
from bs4 import BeautifulSoup

async def watcher(client,discord,asyncio):

    print("[Rank Watcher Task]: Started\n")

    while True:
        delay = 30
        print(f"[Rank Watcher Task]: Stopped for {delay}")
        await asyncio.sleep(delay)
        print("[Rank Watcher Task]:Looping again...")
        players_list = get_players_data()
        if(len(players_list) >0):
            for player in players_list:
                print(f'\n [Rank Watcher Task]: Checking {player["player_name"]}\'s stats \n')
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{player["player_name"]} | {player["faction_name"]}\'s {player["faction_rank"]}'))
                await asyncio.sleep(delay)
                guild = client.get_guild(player["player_guild_id"])
                member = guild.get_member(player["player_discord_id"])
                if(bool(member)):
                    await asyncio.sleep(0)
                    is_valid_faction_member={}
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f'https://www.rpg.b-zone.ro/players/faction/{player["player_name"]}') as resp:
                            content = await resp.text()
                            doc = BeautifulSoup(content, "html.parser")
                            if(len(doc.select("#contentPage > div")[0])>1):
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

                                    if(player["faction_name"]=="" and player["faction_rank"]==""):
                                            if(is_valid_faction_member["other_faction"]==0):
                                                if(is_valid_faction_member["faction_name"]=="SFPD"):
                                                    if(is_valid_faction_member["faction_rank"] in ["Officer (1)","Detective (2)","Sergeant (3)","Lieutenant (4)","Captain (5)","Captain (5)","Assistant Chief (6)","Chief (Leader)"]):
                                                        update_player_faction_name(player["player_discord_id"],is_valid_faction_member["faction_name"])
                                                        update_player_faction_rank(player["player_discord_id"],is_valid_faction_member["faction_rank"])
                                                        update_player_other_faction(player["player_discord_id"],is_valid_faction_member["other_faction"])
                                                        await remove_role_function(member,guild)
                                                        role = member.guild.get_role(sfpd_roles["verified"])
                                                        await member.add_roles(role)
                                                        curren__rank_role = member.guild.get_role(get_rank_role(is_valid_faction_member["faction_name"],is_valid_faction_member["faction_rank"]))
                                                        await member.add_roles(curren__rank_role)
                                                        await member.send(embed = role_update_embed_generator(discord,player["player_name"],is_valid_faction_member["faction_name"],is_valid_faction_member["faction_rank"]))
                                                        if(player["player_discord_id"] in [guild.owner_id,339956284205826048,374223751669088256,331861304425971712]):
                                                            print("Admins")
                                                        else:
                                                            await member.edit(nick=player["player_name"])

                                    elif(is_valid_faction_member["other_faction"]!=1):
                                        if(is_valid_faction_member["faction_name"] == player["faction_name"]):
                                            if(is_valid_faction_member["faction_rank"]!= player["faction_rank"]):
                                                    print("[Rank Watcher Task]: Changes detected !")
                                                    faction_rank_update_result = update_player_faction_rank(player["player_discord_id"],is_valid_faction_member["faction_rank"])
                                                    if(faction_rank_update_result):
                                                        await remove_role_function(member,guild)
                                                        curren__rank_role = member.guild.get_role(get_rank_role(is_valid_faction_member["faction_name"],is_valid_faction_member["faction_rank"]))
                                                        await member.add_roles(curren__rank_role)
                                                        await member.send(embed = role_update_embed_generator(discord,player["player_name"],is_valid_faction_member["faction_name"],is_valid_faction_member["faction_rank"]))
                                                        if(player["player_discord_id"] in [guild.owner_id,339956284205826048,374223751669088256,331861304425971712]):
                                                            print("[Rank Watcher Task]:Discord-server Admins")
                                                        else:
                                                            await member.edit(nick=player["player_name"])
                                                    else:
                                                        print("Something wrong with DB")
                                            else:
                                                print("[Rank Watcher Task]: No changes in the rank")

                                    elif(is_valid_faction_member["other_faction"]==1):
                                        if(player["faction_rank"] == "ex_member"):
                                                        faction_rank_update_result = update_player_faction_rank(player["player_discord_id"],"ex_member")
                                                        if(faction_rank_update_result):
                                                                    await remove_role_function(member,guild)
                                                                    role = member.guild.get_role(sfpd_roles["ex_member"])
                                                                    await member.add_roles(role)
                                                                    await member.send(embed = role_update_embed_generator(discord,player["player_name"],player["faction_name"],"Ex-Member"))
                                                                    if(player["player_discord_id"] in [guild.owner_id,339956284205826048,374223751669088256,331861304425971712]):
                                                                        print("[Rank Watcher Task]:Discord-server Admins")
                                                                    else:
                                                                        await member.edit(nick=player["player_name"])


                                                        else:
                                                            print("Something wrong with DB")  

                                        elif(player["faction_rank"] in ["Officer (1)","Detective (2)","Sergeant (3)","Lieutenant (4)","Captain (5)","Captain (5)","Assistant Chief (6)","Chief (Leader)"]):
                                                faction_rank_update_result = update_player_faction_rank(player["player_discord_id"],"ex_member")
                                                if(faction_rank_update_result):
                                                            await remove_role_function(member,guild)
                                                            role = member.guild.get_role(sfpd_roles["ex_member"])
                                                            await member.add_roles(role)
                                                            await member.send(embed = role_update_embed_generator(discord,player["player_name"],player["faction_name"],"Ex-Member"))
                                                            if(player["player_discord_id"] in [guild.owner_id,339956284205826048,374223751669088256,331861304425971712]):
                                                                print("[Rank Watcher Task]:Discord-server Admins")
                                                            else:
                                                                await member.edit(nick=player["player_name"])
                                                else:
                                                    print("Something wrong with DB")
                                                
                                        


                                    else:
                                        print("[Rank Watcher Task]: No changes..")
                
                            elif(len(doc.select("#contentPage > div")[0]) == 1):   
                                print(f'[Rank Watcher Task]: There\'s a change in player name  : [Ref_id :{player["player_discord_id"]} ]')     
                                channel = guild.get_channel(channel_id["sfpd_bot_log_channel"])
                                embed = discord.Embed(
                                    title="Name change-log",
                                    description=f'<@{player["player_discord_id"]}>\'s name has been changed [Old-Name : {player["player_name"]}]'
                                )
                                await channel.send(embed = embed) 
                
                
                else:
                    print("[Rank Watcher Task]: This member is currently not in the server")
        
        
        else:
            print("[Rank Watcher Task]: 0 players")

