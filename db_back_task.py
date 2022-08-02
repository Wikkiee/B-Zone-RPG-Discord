import json
import asyncio
import traceback
from bson import json_util
from database import get_players_data
from datetime import datetime
from unit_functions import guild_id,channel_id



async def backup_task(client,discord):
    log_guild = client.get_guild(guild_id["sfpd"])
    log_channel = log_guild.get_channel(channel_id["sfpd_bot_log_channel"])
    wikkie_id = 491251010656927746
    developer = log_guild.get_member(wikkie_id)
    embed = discord.Embed(
    title="[🔨] SFPD Bot's Error Manager",
    description="An Error occured in the Task : [Database_Backup Task]",
    color=discord.Colour.random()
    )

    print("[Data-Backup Task] : Started\n")    
    try:
        while True:
            delay = 86400
            print(f"[Data-Backup Task] : Delayed for {delay}\n")
            await asyncio.sleep(delay)
            print("[Data-Backup Task] : Getting data from DB\n")
            data = json.loads(json_util.dumps(get_players_data()))
            with open('outputfile.json', 'w+') as fout:
                    json.dump(data, fout)
                    fout.close()
            data_backu_guild = client.get_guild(guild_id["sfpd"])
            data_backup_channel = data_backu_guild.get_channel(channel_id["sfpd_data_backup_channel"])
            wikkie_id = 491251010656927746
            developer = data_backu_guild.get_member(wikkie_id)
            await developer.send(file=discord.File('outputfile.json',filename=f'sfpd_data_backup-{datetime.now().strftime("%x")}.json'))   
            await data_backup_channel.send(file=discord.File('outputfile.json',filename=f'sfpd_data_backup-{datetime.now().strftime("%x")}.json'))
            print("[Data-Backup Task] : Successfully Saved and sent to backup channel\n")
            print("[Data-Backup Task] : Looping again ...\n")
    except Exception:
        print(traceback.format_exc())
        embed.add_field(name="Error Traceback",value=f"{str(traceback.format_exc())[:1000]}",inline = False)
        await log_channel.send(embed=embed)
        await developer.send(embed=embed)