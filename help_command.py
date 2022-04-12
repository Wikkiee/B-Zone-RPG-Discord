
async def help(discord,client,ctx):
    embed = discord.Embed(
        title="Help commands",
        description = "Test function",
        color = discord.Color.random(),
    )

    embed.add_field(name="Test command",value="test value 1 \n test value 2 \n test value 3",inline=False)
    embed.set_thumbnail(url = client.user.avatar_url)
    await ctx.send(embed=embed)