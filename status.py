import traceback
from unit_functions import guild_id,channel_id

async def status_task(client,asyncio,discord):
    exception_log_guild = client.get_guild(guild_id["sfpd"])
    log_channel = exception_log_guild.get_channel(channel_id["sfpd_bot_log_channel"])
    wikkie_id = 491251010656927746
    developer = exception_log_guild.get_member(wikkie_id)
    embed = discord.Embed(
    title="[🔨] SFPD Bot's Error Manager",
    description="An Error occured in the Task : [Forum_Tracker]",
    color=discord.Colour.random()
    )
    try:
        print("[Status Changer Task]: Started\n")
        while True:
            await client.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.listening, name=f" _WikkiE_#7843"))
            await asyncio.sleep(60)# 10 as in 10seconds
            await client.change_presence(status=discord.Status.idle,activity=discord.Game(name=" with !help"))
            await asyncio.sleep(60)
            await client.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.competing, name=f"Huge new updates"))
            await asyncio.sleep(60)
            await client.change_presence(status=discord.Status.mro,activity=discord.Activity(type=discord.ActivityType.streaming, name=f"use !help to get more info"))
            await asyncio.sleep(60)#Throwing rocks through your windows 
            await client.change_presence(status=discord.Status.idle,activity=discord.Game(name="By Throwing rocks through your windows -Dabrovsky"))
            await asyncio.sleep(60)
            await client.change_presence(status=discord.Status.idle,activity=discord.Game(name="with my FuN#2008"))
            await asyncio.sleep(60)
    except Exception:

        embed.add_field(name="Error Traceback",value=f"{str(traceback.format_exc())}",inline = False)
        await log_channel.send(embed=embed)
        await developer.send(embed=embed)