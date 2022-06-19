
async def help(discord,client,ctx):
    embed = discord.Embed(
        title="Help commands",
        description = "Use `!` as a prefix for all the commands",
        color = discord.Color.random(),
    )

    embed.add_field(name="Players info",value="**`!Playerinfo(pi)` - To check the player stats \n Comming soon \n Comming soon**",inline=True)
    embed.add_field(name="Players info",value="**`!Playerinfo(pi)` - To check the player stats \n Comming soon \n Comming soon**",inline=True)
    embed.set_thumbnail(url = ctx.author.display_avatar)
    await ctx.send(embed=embed)