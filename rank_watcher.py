import aiohttp
from database import get_players_data,update_player_faction_rank,update_player_faction_name,update_player_other_faction
from roles import get_rank_role,sfpd_roles
from unit_functions import remove_role_function ,global_url
async def watcher(client,asyncio):

    print("Rank Watcher Task : Started")

    while True:
        delay = 1
        #print(f"Stopped for {delay}")
        await asyncio.sleep(delay)
        #print("Now resumed....")
        players_list = get_players_data()
        if(len(players_list) >0):
            for player in players_list:
                guild = client.get_guild(player["player_guild_id"])
                role_list = await guild.fetch_roles()
                member = guild.get_member(player["player_discord_id"])
                if(bool(member)):
                    await asyncio.sleep(0)
                    async with aiohttp.ClientSession() as session:
                        site_url = f'{global_url}/verify/{player["player_name"]}'
                        async with session.get(site_url) as resp:
                            is_valid_faction_member =  await resp.json()
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
                                                await member.edit(nick=player["player_name"])

                            elif(is_valid_faction_member["other_faction"]!=1):
                                if(is_valid_faction_member["faction_name"] == player["faction_name"]):
                                    if(is_valid_faction_member["faction_rank"]!= player["faction_rank"]):
                                            print("Changes detected !")
                                            faction_rank_update_result = update_player_faction_rank(player["player_discord_id"],is_valid_faction_member["faction_rank"])
                                            if(faction_rank_update_result):
                                                await remove_role_function(member,guild)
                                                curren__rank_role = member.guild.get_role(get_rank_role(is_valid_faction_member["faction_name"],is_valid_faction_member["faction_rank"]))
                                                await member.add_roles(curren__rank_role)
                                                await member.edit(nick=player["player_name"])
                                            else:
                                                print("Something wrong with DB")
                                    else:
                                        print("No changes in the rank")

                            elif(is_valid_faction_member["other_faction"]==1):
                                if(player["faction_rank"] in ["Officer (1)","Detective (2)","Sergeant (3)","Lieutenant (4)","Captain (5)","Captain (5)","Assistant Chief (6)","Chief (Leader)"]):
                                        faction_rank_update_result = update_player_faction_rank(player["player_discord_id"],"ex_member")
                                        if(faction_rank_update_result):
                                                    await remove_role_function(member,guild)
                                                    role = member.guild.get_role(sfpd_roles["ex_member"])
                                                    await member.add_roles(role)
                                                    await member.edit(nick=player["player_name"])
                                        else:
                                            print("Something wrong with DB")

                            else:
                                print("No changes..")
                else:
                    print("This member is currently not in the server")
        
        
        else:
            print("0 players")

