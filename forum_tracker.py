import traceback
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup 
from database import create_last_announcement_link,update_last_announcement_link,get_last_announcement_link
from unit_functions import guild_id,channel_id,global_url,sfpd_roles,forum_tracker_post_embed


async def tracker(client,discord):
    log_guild = client.get_guild(guild_id["sfpd"])
    log_channel = log_guild.get_channel(channel_id["sfpd_bot_log_channel"])
    wikkie_id = 491251010656927746
    developer = log_guild.get_member(wikkie_id)
    embed = discord.Embed(
    title="[🔨] SFPD Bot's Error Manager",
    description="An Error occured in the Task : [Forum_Tracker]",
    color=discord.Colour.random()
    )
    
        
    try:
        print("[Forum Tracker Task] : Started\n")
        print(f'Forum Tracker Task : Collection creation result - {create_last_announcement_link()}')
        while True:
            last_link = get_last_announcement_link()
            delay = 30
            print(f"[Forum Tracker Task]: Stopped for {delay}")
            await asyncio.sleep(delay)
            print("[Forum Tracker Task]:Looping again..")
            guild = client.get_guild(guild_id["sfpd"])
            channel = client.get_channel(channel_id["sfpd_announcement"])
            async with aiohttp.ClientSession() as session:
                                login_url = "https://forum.b-zone.ro/login/"
        
                                notification_url ="https://forum.b-zone.ro/notifications/"

                                with requests.session() as s:
                                        data  = s.get("https://forum.b-zone.ro/login/")
                                        
                                        doc = BeautifulSoup(data.text ,"html.parser")
                                        payload = {
                                        "csrfKey": doc.select('#ipsLayout_mainArea > form > input[type=hidden]:nth-child(1)')[0]["value"],
                                        "ref": "aHR0cHM6Ly9mb3J1bS5iLXpvbmUucm8vP19mcm9tTG9nb3V0PTEmX2Zyb21Mb2dpbj0x",
                                        "auth":"wiwehew915@weepm.com",
                                        "password":"discordbot1",
                                        "remember_me":1,
                                        "_processLogin":"usernamepassword"

                                        }
                                        r1 = s.post(login_url,data=payload)
                                        print("[Forum Tracker Task]:Logged into forum")
                                        content = s.get(notification_url)
                                        doc = BeautifulSoup(content.text ,"html.parser")
                        
                                        faction_forum_name=""
                                        forum_topic_name=""
                                        forum_post_link=""
                                        post_author=""
                                        dm= 0
                                        announce_val= 0
                                        other_data=0
                                        print("[Forum Tracker Task]:Collecting data")
                                        topic_name = doc.select("#ipsLayout_mainArea > div.ipsBox > ol > li:nth-child(1) > div.ipsDataItem_main > a")[0].string.strip()
                                        forum_post_link = doc.select("#ipsLayout_mainArea > div.ipsBox > ol > li:nth-child(1) > div.ipsDataItem_main > a")[0]["href"]
                                        temp = topic_name.split(" ")
                                        for word in temp:
                                            if(word == "commented"):
                                                break
                                            else:
                                                post_author = post_author + " " + word
                                            
                                        if "SF Police Department" in topic_name:
                                            print("[Forum Tracker Task]: Selected SFPD Forum page ...")
                                            faction_forum_name = "SF Police Department"
                                            if("Discussions" in topic_name):
                                                topic_name = "Discussions"
                                                other_data = 1
                                            elif("Anunţuri Importante / Important Announcements" in topic_name):
                                                forum_topic_name = "Anunţuri Importante / Important Announcements"
                                                dm = 0
                                                announce_val = 1
                                            elif("Transfer Echipe / Team Transfer" in topic_name):
                                                if("dabro.pdf" in post_author):
                                                    other_data = 1
                                                else:
                                                    forum_topic_name = "Transfer Echipe / Team Transfer"
                                                    dm = 1
                                                
                                            elif("Log Echipe / Team Logs" in topic_name):
                                                if("dabro.pdf" in post_author):
                                                    other_data = 1
                                                else:
                                                    forum_topic_name = "Log Echipe / Team Logs"
                                                    dm = 1 
                                            elif("Sugestii / Suggestions" in topic_name):
                                                if("dabro.pdf" in post_author):
                                                    other_data = 1
                                                else:
                                                    forum_topic_name = "Sugestii / Suggestions"
                                                    dm = 1
                                        else:
                                            print("[Forum Tracker Task]: SFPD Page not found")
                                            other_data=1

                                        forum_post_data = {
                                        "other_data":other_data,
                                        "faction_name":faction_forum_name,
                                        "forum_topic":forum_topic_name,
                                        "post_link":forum_post_link,
                                        "author_name" : post_author,
                                        "dm_dabro":dm,
                                        "announce" : announce_val
                                        }
                                        print(forum_post_data)
                                        if(forum_post_data["other_data"] == 0):
                                            if(last_link == forum_post_data["post_link"]):
                                                print("Forum Tracker Task : No new message detected")
                                            else:
                                                if(forum_post_data["dm_dabro"] == 1):
                                                    update_last_announcement_link(forum_post_data["post_link"])
                                                    dabro = client.get_user(339956284205826048)
                                                    await dabro.send(embed = forum_tracker_post_embed(forum_post_data))
                                                elif(forum_post_data["announce"] == 1):
                                                    update_last_announcement_link(forum_post_data["post_link"])
                                                    # last_link = forum_post_data["post_link"]
                                                    await channel.send(f'<@&{sfpd_roles["verified"]}>',embed = forum_tracker_post_embed(forum_post_data))
                                        else: #f'<@&{sfpd_roles["verified"]}>',
                                            print("[Forum Tracker Task]: No new data ... back to loog")
    except Exception:
        print(traceback.format_exc())
        embed.add_field(name="Error Traceback",value=f"{str(traceback.format_exc())}",inline = False)
        await log_channel.send(embed=embed)
        await developer.send(embed=embed)