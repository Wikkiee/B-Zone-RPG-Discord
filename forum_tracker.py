from ast import While
from unit_functions import guild_id,channel_id,global_url,sfpd_roles
import aiohttp
import asyncio

async def tracker(client,discord):
    print("Forum Tracker Task : Started")
    last_link = 'https://forum.b-zone.ro/topic/245545-sf-school-instructors-discussions/?do=findComment&comment=705369'
    while True:
        await asyncio.sleep(10)
        guild = client.get_guild(guild_id["sfpd"])
        channel = guild.get_channel(channel_id["sfpd_announcement"])
        # await channel.send("Hello")
        async with aiohttp.ClientSession() as session:
                            site_url = f'{global_url}/forum/'
                            async with session.get(site_url) as resp:
                                forum_post_data =  await resp.json()
                                if(last_link == forum_post_data["post_link"]):
                                    print("No new messages")
                                else:
                                    last_link = forum_post_data["post_link"]
                                    embed = discord.Embed(
                                    title= f'**{forum_post_data["faction_name"]}**',
                                    description=f'**Topic : {forum_post_data["forum_topic"]}**' ,
                                    color=discord.Colour.random(),
                                    url=forum_post_data["post_link"]
                                    )
                                    embed.add_field(name=f'[📣] New Content by {forum_post_data["author_name"]}',value=f'_New content has been posted on forum. Follow up link here: [click me]({forum_post_data["post_link"]}) \n <@&{sfpd_roles["verified"]}>_',inline=False)
                                    
                                    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
                                    await channel.send(f'<@&{sfpd_roles["verified"]}>',embed = embed)

