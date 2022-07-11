async def status_task(client,asyncio,discord):
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