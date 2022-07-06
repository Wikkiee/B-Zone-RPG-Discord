
async def help(discord,client,ctx):
    embed = discord.Embed(
        title="[🏆] B-zone RPG",
        description = """These are the features of B-zone RGP Bot if you have problems(bugs) with it or have any suggestions ,Please let me know using \n `!suggestions <your_Message>` \t \t \t
》
》""",
        color = discord.Color.random(),
    )

    embed.add_field(name="[🕵️‍♂️] Players Commands",value="**`!id <RPG_player_name>`** - _To get the current status of a player _ ",inline=False)
    embed.add_field(name="[🎯] Faction Commands",value=" **`!factions`** - _To get the Factions list and it's status_ \n**`!sverify`** - _To sync your Discord ID with your RPG Account to keep track on your Ranks (Works only on #verification Text-Channel)_ \n**`!forum`** - _To get the link of all important forum topics_",inline=False)
    embed.add_field(name="[👮‍♂️] Staff Commands",value=" **`!Helpers`** _To get the current status of a STAFFS _ \n**`!leaders`** _To get the current status of a leaders_",inline=False)
    embed.add_field(name="[🎈] Utilities Commands",value="**`!pfp <@mention>`** _To view the members profile pic_ \n**`#imgur-area`** - _Drop your pics and get uploaded permanent shareable link_",inline=False)
    embed.add_field(name="[💖] B-zone Supports",value="[Vist RPG Site](https://www.rpg.b-zone.ro/) | [Forum](https://forum.b-zone.ro/) | [Discord](https://discord.gg/qtXwDC2H) | [Contact](https://discord.gg/fKDbRTuTpe) ",inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/961691415400820776/993049804793974914/ezgif.com-gif-maker_4.gif")
    embed.set_thumbnail(url=client.user.avatar)
    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
    await ctx.send(embed=embed)