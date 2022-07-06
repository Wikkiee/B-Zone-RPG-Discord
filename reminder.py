import calendar
import datetime
from unit_functions import get_training_reminder_announcement_embed,channel_id
import asyncio

async def training_reminder(client):
    print("Status Changer Task : Started")
    while True:
        print("Delayed for : 60 sec")
        await asyncio.sleep(60)
        c = calendar.Calendar(firstweekday=calendar.MONDAY)

        current_year = datetime.datetime.now()
        year = int(current_year.strftime("%Y"))
        current_month = datetime.datetime.now()
        month = int(current_month.strftime("%m"))
        monthcal = c.monthdatescalendar(year,month)
        first_and_third_sunday = [day for week in monthcal for day in week if \
                        day.weekday() == calendar.SUNDAY and \
                        day.month == month]
        print(first_and_third_sunday[0])
        print(first_and_third_sunday[2])
        
        date = datetime.datetime.now()
        today_date = date.strftime("%d")
        this_month = date.strftime("%m")
        this_year = date.strftime("%Y")
        
        print("Today's Date : ",this_year,this_month,today_date)
        print(str(first_and_third_sunday[0])[8:])
        print(str(first_and_third_sunday[2])[8:])
        if(this_year == str(first_and_third_sunday[0])[:4] and this_month == str(first_and_third_sunday[0])[5:7]):
            channel = client.get_channel(channel_id["sfpd_announcement"])
            if(today_date == str(first_and_third_sunday[0])[8:]):
                await channel.send('<@&990547306694713394>',embed = get_training_reminder_announcement_embed(f'{today_date}-{this_month}-{this_year}',"15:00"))
            elif("17" == str(first_and_third_sunday[2])[8:]):
                await channel.send('<@&990547306694713394>',embed = get_training_reminder_announcement_embed(f'{today_date}-{this_month}-{this_year}',"20:00"))
            else:
                print("Not a first or third sunday")
        elif(this_year == str(first_and_third_sunday[2])[:4] and this_month == str(first_and_third_sunday[2])[5:7]):
            print("err")