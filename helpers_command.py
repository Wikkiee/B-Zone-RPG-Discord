async def helpers(data,discord,ctx):
        helpers_embed = discord.Embed(
            title="[👨‍✈️] Staffs info",
            description="_These are the current status of all the Helpers & Admins",
            color=discord.Color.random(),
            url="https://www.rpg.b-zone.ro/staff/helpers"
        )        
        def helpers_details_with_escape_seq_converter(faction_type,data,argument):
            temp_name_list = []
            temp_current_status_list = []
            temp_last_login_list = []
            for i in range(0,len(data[faction_type])):
                temp_name_list.append(data[faction_type][i]["name"]) 
                temp_current_status_list.append(data[faction_type][i]["current_status"]) 
                temp_last_login_list.append(data[faction_type][i]["last_login"])
            if(argument == "name"):  
                return "              \n              ".join(temp_name_list)
            elif(argument == "current_status"):
                return "              \n              ".join(temp_current_status_list)
            elif(argument == "last_login"):
                return "              \n              ".join(temp_last_login_list)

        
        helpers_embed.add_field(name="   Level 1 Helpers   ",value="{}".format(helpers_details_with_escape_seq_converter("level_1_helpers",data,"name")) ,inline=True)
        helpers_embed.add_field(name="   Currently   ",value="{}".format(helpers_details_with_escape_seq_converter("level_1_helpers",data,"current_status")) ,inline=True)
        helpers_embed.add_field(name="   Last Login   ",value="{}".format(helpers_details_with_escape_seq_converter("level_1_helpers",data,"last_login")) ,inline=True)
        helpers_embed.add_field(name="   Level 2 Helpers   ",value="{}".format(helpers_details_with_escape_seq_converter("level_2_helpers",data,"name")) ,inline=True)
        helpers_embed.add_field(name="   Currently   ",value="{}".format(helpers_details_with_escape_seq_converter("level_2_helpers",data,"current_status")) ,inline=True)
        helpers_embed.add_field(name="   Last Login   ",value="{}".format(helpers_details_with_escape_seq_converter("level_2_helpers",data,"last_login")) ,inline=True)
        helpers_embed.add_field(name="   Level 3 Helpers/Admins   ",value="{}".format(helpers_details_with_escape_seq_converter("level_3_helpers",data,"name")) ,inline=True)
        helpers_embed.add_field(name="   Currently   ",value="{}".format(helpers_details_with_escape_seq_converter("level_3_helpers",data,"current_status")) ,inline=True)
        helpers_embed.add_field(name="   Last Login   ",value="{}".format(helpers_details_with_escape_seq_converter("level_3_helpers",data,"last_login")) ,inline=True)
        helpers_embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/f432105e485288211f56b42f6e5e1d16.png?size=1024")
        await ctx.reply(embed = helpers_embed)