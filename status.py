async def status_task(client,asyncio,discord):
    print("Status Changer Task : Started")
    while True:
        await client.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.listening, name=f" Wikkie"))
        await asyncio.sleep(30)# 10 as in 10seconds
        await client.change_presence(status=discord.Status.idle,activity=discord.Game(name=" with !help"))
        await asyncio.sleep(30)
        await client.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.competing, name=f"Huge new updates"))
        await asyncio.sleep(30)
        await client.change_presence(status=discord.Status.mro,activity=discord.Activity(type=discord.ActivityType.streaming, name=f"use !help to get more info"))
        await asyncio.sleep(30)