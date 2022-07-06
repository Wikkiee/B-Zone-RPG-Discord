from email.mime import image
from roles import sfpd_roles
import discord
async def remove_role_function(member,guild):
    role_list = member.roles
    role_list = list(role_list)
    ignore_roles_list = [sfpd_roles["verified"],990488671553716244,990484473080582205]
    for role in role_list:
        if(role.id in ignore_roles_list ):
            pass
        else:
            remove_role = guild.get_role(role.id)
            await member.remove_roles(remove_role)

global_url = "https://bzone-rpg-api.herokuapp.com"

# global_url = 'http://localhost:3000'

guild_id = {
    "sfpd":990484473080582205,
    "sfsi":"d"
}

channel_id = {
    "sfpd_imgur":990562699056402462,
    "sfpd_announcement":990561385412968448,
    "sfpd_verification_channel":990485622403788841,
    "sfpd_suggestion_channel_id":993778808090021998
}

def role_update_embed_generator(discord,name,faction,rank):
    description = ""
    if(faction != "Other" and rank != "Ex-Member"):
        description = f'_Hey {name}, your roles has been updated with respect to your current {faction} faction rank [{rank}]_'

    elif(rank == "Ex-Member"):
        description = f'_Hey {name}, it seems you have resigned from {faction} Faction, so i have updated your role as [{rank}]_'
    elif(faction == "Other"):
        description = f'_Hey {name}, it seems you never been a part of {faction}, so i have updated your role as [{rank}]_'
    embed = discord.Embed(
    title="**Role Update**",
    description=description,
    color=discord.Colour.random()
    )
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    return embed

def imagur_upload_embed_generator(discord,title,description,dm=False,album_link=None):
        embed = discord.Embed(title=f'**{title}**',
        description=f'_{description}_',
        color=discord.Colour.random()
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        if(dm):
            embed.add_field(name="[🔗] POST LINK",value=f'**Album** - `{album_link["album_post_link"]}` | [View]({album_link["album_post_link"]})',inline=False)
            embed.set_image(url=album_link["first_image_link"])
        return embed

def get_training_reminder_announcement_embed(date,time):
    embed = discord.Embed(
        title="[📣] SFPD Training session reminder",
        description=f'**ATTENTION! On Sunday ( {date} ) at {time} (server time) **\n_we will have a 40 to 60 minutes training session (depending on the organizer\'s plan) with mandatory presence!_',
        color=discord.Colour.random()
    )
    embed.add_field(name="Keep in mind the following list of penalties, depending on your arrival:",value=">>> - Being late for 10 minutes or less = nothing;\n- Being for 10-20 minutes = Verbal Warning;\n- Being for 20-30 minutes = Verbal Warning + a 50.000$ fine;\n- Being late for 30+ minutes = Faction Warn." ,inline=False)
    embed.add_field(name="Note :",value="You have the possibility to opt out of a maximum of one activity this month. Visit the following to submit the pass request: [[Click Me](https://forum.b-zone.ro/topic/384352-sf-police-department-învoiri-pass-requests/)]",inline=False)
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    return embed