import json
import asyncio
import traceback
from bson import json_util
from database import get_players_data
from datetime import datetime

async def backup_task(client,discord):
    # guild = client.get_guild(guild_id["sfpd"])
    # channel = guild.get_channel(channel_id["sfpd_bot_log_channel"])
    guild = client.get_guild(959138134413684836)
    log_channel = guild.get_channel(990242620687122462)
    wikkie_id = 491251010656927746
    developer = guild.get_member(wikkie_id)
    embed = discord.Embed(
    title="[🔨] SFPD Bot's Error Manager",
    description="An Error occured in the Task : [Database_Backup Task]",
    color=discord.Colour.random()
    )

    print("[Data-Backup Task] : Started\n")    
    try:
        while True:
            delay = 60

            print(f"[Data-Backup Task] : Delayed for {delay}\n")
            await asyncio.sleep(delay)
            print("[Data-Backup Task] : Getting data from DB\n")
            def parse_json(data):
                return json.loads(json_util.dumps(data))
            data = parse_json(get_players_data())

            async def create_json():
                with open('outputfile.json', 'w+') as fout:
                    json.dump(data, fout)
                    guild = client.get_guild(959138134413684836)
                    log_channel = guild.get_channel(990242620687122462)
                    wikkie_id = 491251010656927746
                    developer = guild.get_member(wikkie_id)
                    fout.close()
                    file = discord.File('outputfile.json',filename=f'sfpd_data_backup-{datetime.now().strftime("%x")}.json',spoiler=True)
                    await developer.send("",file=file)   
                    await log_channel.send("**Data-Backup File**",file=file)
                    print("[Data-Backup Task] : Successfully Saved and sent to backup channel\n")
            await create_json()
            print("[Data-Backup Task] : Looping again ...\n")
    except Exception:
        print(traceback.format_exc())
        embed.add_field(name="Error Traceback",value=f"{str(traceback.format_exc())[:1000]}",inline = False)
        await log_channel.send(embed=embed)
        await developer.send(embed=embed)