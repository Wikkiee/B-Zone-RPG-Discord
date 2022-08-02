import calendar
import datetime
import traceback
from unit_functions import get_training_reminder_announcement_embed,channel_id,guild_id
import asyncio
from roles import sfpd_roles
from datetime import datetime

async def training_reminder(client,discord):

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
        print("[Training Reminder Task] : Started\n")
        while True:
            print("Delayed for : 3600 sec")
            await asyncio.sleep(3600)
            c = calendar.Calendar(firstweekday=calendar.MONDAY)

            current_year = datetime.now()
            year = int(current_year.strftime("%Y"))
            current_month = datetime.now()
            month = int(current_month.strftime("%m"))
            monthcal = c.monthdatescalendar(year,month)
            first_and_third_sunday = [day for week in monthcal for day in week if \
                            day.weekday() == calendar.SUNDAY and \
                            day.month == month]
            print(first_and_third_sunday[0])
            print(first_and_third_sunday[2])
            
            date = datetime.now()
            today_date = date.strftime("%d")
            this_month = date.strftime("%m")
            this_year = date.strftime("%Y")
            time = datetime.now()
            time = time.strftime("%X")
            print(f'Training Reminder Task : Date : {today_date}/{this_month}/{this_year} | Time : {time[:2]}')
            if(this_year == str(first_and_third_sunday[0])[:4] and this_month == str(first_and_third_sunday[0])[5:7]):
                channel = client.get_channel(channel_id["sfpd_reminder_channel"])
                if(time[:2] == "10"):
                    if(today_date == str(first_and_third_sunday[0])[8:]):
                        await channel.send(f'<@&{sfpd_roles["verified"]}>',embed = get_training_reminder_announcement_embed(f'{today_date}-{this_month}-{this_year}',"15:00"))
                    elif(today_date == str(first_and_third_sunday[2])[8:]):
                        await channel.send(f'<@&{sfpd_roles["verified"]}>',embed = get_training_reminder_announcement_embed(f'{today_date}-{this_month}-{this_year}',"20:00"))
                    else:
                        print("Not a first or third sunday")
    except Exception:

        embed.add_field(name="Error Traceback",value=f"{str(traceback.format_exc())}",inline = False)
        await log_channel.send(embed=embed)
        await developer.send(embed=embed)