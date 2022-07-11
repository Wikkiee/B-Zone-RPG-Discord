async def leaders(data,discord,ctx,total_execution_time):
        leaders_embed = discord.Embed(
            title="[👑] Leaders info",
            description="_These are the current status of all the Leaders",
            color=discord.Color.random(),
            url="https://www.rpg.b-zone.ro/staff/leaders"
        )        
        def leaders_details_with_escape_seq_converter(faction_type,data,argument):
            temp_name_list = []
            temp_faction_list = []
            temp_last_login_list = []
            for i in range(0,len(data[faction_type])):
                temp_name_list.append(data[faction_type][i]["name"]) 
                temp_faction_list.append(data[faction_type][i]["faction"]) 
                temp_last_login_list.append(data[faction_type][i]["last_login"])
            if(argument == "name"):  
                return "              \n              ".join(temp_name_list)
            elif(argument == "faction"):
                return "              \n              ".join(temp_faction_list)
            elif(argument == "last_login"):
                return "              \n              ".join(temp_last_login_list)

        
        leaders_embed.add_field(name="   Leader Name   ",value="{}".format(leaders_details_with_escape_seq_converter("Peaceful_faction",data,"name")) ,inline=True)
        leaders_embed.add_field(name="   Faction   ",value="{}".format(leaders_details_with_escape_seq_converter("Peaceful_faction",data,"faction")) ,inline=True)
        leaders_embed.add_field(name="   Last Login   ",value="{}".format(leaders_details_with_escape_seq_converter("Peaceful_faction",data,"last_login")) ,inline=True)
        leaders_embed.add_field(name="   Leader Name   ",value="{}".format(leaders_details_with_escape_seq_converter("gang_factions",data,"name")) ,inline=True)
        leaders_embed.add_field(name="   Faction   ",value="{}".format(leaders_details_with_escape_seq_converter("gang_factions",data,"faction")) ,inline=True)
        leaders_embed.add_field(name="   Last Login   ",value="{}".format(leaders_details_with_escape_seq_converter("gang_factions",data,"last_login")) ,inline=True)
        leaders_embed.add_field(name="   Leader Name   ",value="{}".format(leaders_details_with_escape_seq_converter("department_factions",data,"name")) ,inline=True)
        leaders_embed.add_field(name="   Faction   ",value="{}".format(leaders_details_with_escape_seq_converter("department_factions",data,"faction")) ,inline=True)
        leaders_embed.add_field(name="   Last Login   ",value="{}".format(leaders_details_with_escape_seq_converter("department_factions",data,"last_login")) ,inline=True)
        leaders_embed.set_footer(text=f'{total_execution_time} | use `!help` to know more |use !suggestions to share your ideas',icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
        await ctx.reply(embed = leaders_embed)