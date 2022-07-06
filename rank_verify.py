
from calendar import c
from http import client
import traceback
from discord.ui import View,Button
from database import insert_users_data
from roles import get_rank_role,sfpd_roles


async def verify(discord,ctx,data,player_name):
    try:
        print(data)
        embed = discord.Embed(
            title="[🏆] Verified Successfully",
            description = "Your rank has been setted and it'll be automatically update..." ,
            color = discord.Color.random(),
        )
        embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        if(data["other_faction"]==0):
            add_data = {
                        "player_name" : player_name,
                        "player_discord_id":ctx.author.id,
                        "player_guild_id":ctx.guild.id,
                        "faction_name":data["faction_name"],
                        "faction_rank":data["faction_rank"],
                        "faction_warn":data["faction_warn"],

                    }   
            insertion_result = insert_users_data(add_data)
        elif(data["other_faction"]==1):
            add_data = {
                        "player_name" : player_name,
                        "player_discord_id":ctx.author.id,
                        "player_guild_id":ctx.guild.id,
                        "faction_name":"",
                        "faction_rank":"",
                        "faction_warn":"",
                        "other_faction":1,
                    }   
            insertion_result = insert_users_data(add_data)

        # rank_1_role = ctx.guild.get_role(990485217506631741)

        if(insertion_result):
            print("Inserted")
            if(data["other_faction"]==0):
                if(ctx.guild.owner_id == ctx.message.author.id):
                    print("check 2")
                    nick_name_error_embed = discord.Embed(
                        title="[❗] Error",
                        description = "Your rank has been setted but i don't have permission to change your name." ,
                        color = discord.Color.random(),
                        )
                    nick_name_error_embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
                    await ctx.reply(embed = nick_name_error_embed)
                else:
                    await ctx.message.author.edit(nick=player_name)
                    role_id = get_rank_role(data["faction_name"],data["faction_rank"])
                    print(role_id)
                    member = ctx.message.author
                    print(member)
                    await member.add_roles(ctx.message.guild.get_role(990547306694713394))
                    await member.add_roles(ctx.message.guild.get_role(role_id))
                    # await ctx.author.add_roles(ctx.guild,ctx.author,"verified")
                    await ctx.reply(embed=embed)
            elif(data["other_faction"]==1):
                    member = ctx.message.author
                    role = member.guild.get_role(sfpd_roles["other_faction_members"])
                    await member.add_roles(role)
                    await member.edit(nick=player_name)
        else:
            print("Error_1")

    
    except Exception as e:
        print(traceback.format_exc())
        print("Errors_2")
        print(e.__class__)


































        # embed = discord.Embed(
        # title="**Welcome to SFSI Setup portal**",
        # description="Click the Accept button to proceed",
        # color=discord.Colour.random()
        # )
        # embed.add_field(name ="Things gonna Add" ,value="SFSI Rank 0 - 6 Roles  \nSFSI Weekly Mission Channel")
        # embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        # await ctx.reply(embed = embed)

        # sfsi_manager_accept_button = Button(label="Accept",style=discord.ButtonStyle.primary,emoji="✅",custom_id="acceptButton")
        # view = View()
        # view.add_item(sfsi_manager_accept_button)

        # async def on_accept_button_click(interaction):
        #         embed = discord.Embed(
        #                 title="test"
        #         )
        #         rank_1 = await ctx.guild.create_role(name="Rank 2",colour=discord.Colour(0x18FD08),hoist=True,mentionable=True)
        #         await ctx.author.add_roles(temp)
        #         view.clear_items()
        #         await interaction.response.send_message(temp)

        # sfsi_manager_accept_button.callback = on_accept_button_click

        # await ctx.reply(embed=embed,view=view)