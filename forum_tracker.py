from unit_functions import guild_id,channel_id,global_url,sfpd_roles,forum_tracker_post_embed
import aiohttp
import asyncio
from database import create_last_announcement_link,update_last_announcement_link,get_last_announcement_link

async def tracker(client,discord):
    print("[Forum Tracker Task] : Started\n")
    print(f'Forum Tracker Task : Using {global_url} for fetching data')
    print(f'Forum Tracker Task : Collection creation result - {create_last_announcement_link()}')
    while True:
        last_link = get_last_announcement_link()
        delay = 10
        print(f"[Forum Tracker Task]: Stopped for {delay}")
        await asyncio.sleep(delay)
        print("[Forum Tracker Task]:Looping again..")
        guild = client.get_guild(guild_id["sfpd"])
        channel = client.get_channel(channel_id["sfpd_announcement"])
        async with aiohttp.ClientSession() as session:
                            site_url = f'{global_url}/forum/'
                            async with session.get(site_url) as resp:
                                forum_post_data =  await resp.json()
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
                                            await channel.send(embed = forum_tracker_post_embed(forum_post_data))
                                else: #f'<@&{sfpd_roles["verified"]}>',
                                    print("[Forum Tracker Task]: No new data ... back to loog")
