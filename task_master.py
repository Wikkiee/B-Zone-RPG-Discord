from cmath import log
from rank_watcher import watcher
from unit_functions import guild_id,channel_id
async def task_master(client,discord,asyncio):
    print("[Task Master Task]: Started\n")

    delay = 10
    while True:
        print(f"[Task Master Task]: Stopped for {delay}")
        await asyncio.sleep(delay)
        all_tasks = asyncio.all_tasks()
        all_tasks_name_list = []
        for i in all_tasks:
            if(i.get_name() != "Task-1"):
                all_tasks_name_list.append(i.get_name())
        log_guild = client.get_guild(guild_id["sfpd"])
        log_channel = log_guild.get_channel(channel_id["sfpd_bot_log_channel"])
        if('watcher' in all_tasks_name_list):
            print("Running")#995969103162519572
        else:
            client.loop.create_task(watcher(client,discord,asyncio),name="watcher")
            await log_channel.send("**Rank Watcher stopped working...**")
            await asyncio.sleep(3)
            await log_channel.send("**Restarting Rank Watcher...**")
            await asyncio.sleep(3)
            await log_channel.send("**Done...**")