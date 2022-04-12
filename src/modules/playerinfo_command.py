
import discord
from discord.ui import View,Button






async def playerinfo_func(discord,ctx,data):
    view = View()
    if (data["playerFound"] == 1):
        player_info_embed = discord.Embed(
            title="{}'s info".format(data["ign"]),
            description="**Currently : {} ** | ** Last login : {} **".format(data["current_status"],data["last_login"]),
            color=discord.Color.random(),
            url=data["profile_url"]
        )

        faction_info_embed = discord.Embed(
            title="{}'s Faction".format(data["ign"]),
            description="**Currently : {} ** | ** Last login : {} **".format(data["current_status"],data["last_login"]),
            color=discord.Color.random(),
            url= "https://www.rpg.b-zone.ro/{}".format(data['faction_url']) if data["faction_name"] != "Civilian" else None
        )





        player_info_embed.set_image(url=data["avatar_url"])
        player_info_embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.display_avatar)
        player_info_embed.add_field(name="Level",value="**`{}`**".format(data['level']),inline=True)
        player_info_embed.add_field(name="Respect",value="**`{}`**".format(data["respect"]),inline=True)
        player_info_embed.add_field(name="Hours played",value="**`{}`**".format(data["hours_played"]),inline=True)
        player_info_embed.add_field(name="Hours played this month",value="**`{}`**".format(data["hours_played_this_month"]),inline=True)
        player_info_embed.add_field(name="RHours played this month",value="**`{}`**".format(data["real_hours_this_month"]),inline=True)
        player_info_embed.add_field(name="Married / Status",value="**`{}`**".format(data["married"]),inline=True)
        player_info_embed.set_footer(text="Made with ❤ by Wikkie#7843",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/91024a720ff49b19560fa1e39ee85583.webp?size=1024")

        faction_info_embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.display_avatar)
        faction_info_embed.add_field(name="Faction Name",value="**`{}`**".format(data["faction_name"]),inline=True)
        faction_info_embed.add_field(name="Join Date",value="**`{}`**".format(data["join_date"]),inline=True)
        faction_info_embed.add_field(name="Rank",value="**`{}`**".format(data["rank"]),inline=True)
        faction_info_embed.add_field(name="Faction Punish",value="**`{}`**".format(data["faction_punish"]),inline=True)
        faction_info_embed.add_field(name="Faction warns",value="**`{}`**".format(data["faction_warns"]),inline=True)
        faction_info_embed.add_field(name="Faction Time",value="**`{}`**".format(data["faction_time"]),inline=True)

        # faction_info_embed.add_field(name="Recent Faction Logs",value="**Date \t Leader \t Faction \t Action\n{} \t {} \t {} \t {}\n**".format(data["faction_log"][0][1],data["faction_log"][1][1],data["faction_log"][2][1],data["faction_log"][3][1]),inline=False)
        faction_info_embed.set_footer(text="Made with ❤ by Wikkie#7843",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/91024a720ff49b19560fa1e39ee85583.webp?size=1024")





        faction_button = Button(label="Faction",style=discord.ButtonStyle.primary,emoji="📑",custom_id="generalButton")
        general_button = Button(label="General info",style=discord.ButtonStyle.primary,emoji="📑",custom_id="factionButton")
        view.add_item(faction_button)
    
        async def faction_cb(interaction): 
            view.clear_items()
            view.add_item(general_button)
            await interaction.response.edit_message(embed = faction_info_embed,view = view)
        faction_button.callback = faction_cb
        async def general_cb(interaction):
            view.clear_items()
            view.add_item(faction_button)
            await interaction.response.edit_message(embed = player_info_embed,view = view)
        general_button.callback = general_cb

        if(data["faction_name"] != "Civilian"):
            faction_info_embed.set_image(url=data["faction_logo_url"])
        else:
            print("Player isn't in a faction")

    else:
        player_info_embed = discord.Embed(
        color=discord.Color.random()
        )
        player_info_embed.add_field(name="Oops",
        value="Player not found, Please enter the valid name",inline=True)
        view = None

    await ctx.reply(embed=player_info_embed,view = view)












        # embed.add_field(name="**Licenses**",value="",inline=False)
    # embed.add_field(name="Driving licenses",value=data["driving_lic"],inline=True)
    # embed.add_field(name="Flying licenses",value=data["flying_lic"],inline=True)
    # embed.add_field(name="Sailing licenses",value=data["sailing_lic"],inline=True)
    # embed.add_field(name="Fishing licenses",value=data["fishing_lic"],inline=True)
    # embed.add_field(name="Weapon licenses",value=data["weapon_lic"],inline=True)
    # embed.add_field(name="Materials licenses",value=data["materials_lic"],inline=True)