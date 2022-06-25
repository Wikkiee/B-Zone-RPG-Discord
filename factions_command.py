async def factions(data,discord,ctx):
        faction_embed = discord.Embed(
            title="[🎯] Factions info",
            description="_These are the current status of all the Factions_",
            color=discord.Color.random(),
            url="https://www.rpg.b-zone.ro/factions/index"
        )        
        def faction_details_with_escape_seq_converter(faction_type,data,argument):
            temp_name_list = []
            temp_members_list = []
            temp_status_list = []
            for i in range(0,len(data[faction_type])):
                temp_name_list.append(data[faction_type][i]["name"]) 
                temp_members_list.append(data[faction_type][i]["members"]) 
                if(data[faction_type][i]["status"] == "lock_open"):
                    temp_status_list.append("Open")
                else:
                    temp_status_list.append("Closed")
            if(argument == "name"):  
                return "              \n              ".join(temp_name_list)
            elif(argument == "members"):
                return "              \n              ".join(temp_members_list)
            elif(argument == "status"):
                return "              \n              ".join(temp_status_list)

        
        faction_embed.add_field(name="   Faction Name   ",value="{}".format(faction_details_with_escape_seq_converter("Peaceful_faction",data,"name")) ,inline=True)
        faction_embed.add_field(name="   Members   ",value="{}".format(faction_details_with_escape_seq_converter("Peaceful_faction",data,"members")) ,inline=True)
        faction_embed.add_field(name="   Status   ",value="{}".format(faction_details_with_escape_seq_converter("Peaceful_faction",data,"status")) ,inline=True)
        faction_embed.add_field(name="   Faction Name   ",value="{}".format(faction_details_with_escape_seq_converter("gang_factions",data,"name")) ,inline=True)
        faction_embed.add_field(name="   Members   ",value="{}".format(faction_details_with_escape_seq_converter("gang_factions",data,"members")) ,inline=True)
        faction_embed.add_field(name="   Status   ",value="{}".format(faction_details_with_escape_seq_converter("gang_factions",data,"status")) ,inline=True)
        faction_embed.add_field(name="   Faction Name   ",value="{}".format(faction_details_with_escape_seq_converter("department_factions",data,"name")) ,inline=True)
        faction_embed.add_field(name="   Members   ",value="{}".format(faction_details_with_escape_seq_converter("department_factions",data,"members")) ,inline=True)
        faction_embed.add_field(name="   Status   ",value="{}".format(faction_details_with_escape_seq_converter("department_factions",data,"status")) ,inline=True)
        faction_embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        
        
        
        
        
        
        
        



        await ctx.reply(embed = faction_embed)

