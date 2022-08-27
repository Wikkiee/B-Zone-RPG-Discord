from cProfile import label
from optparse import Values
import aiohttp
from bs4 import BeautifulSoup
from database import is_registered_user
from discord.ui import View,Button,Select

async def add_market_function(ctx,discord):
    print(ctx.author.id)
    is_registered_rpg_discord_user = is_registered_user(ctx.author.id)

    if(bool(is_registered_rpg_discord_user)):
        await ctx.send(f'Player Name : {is_registered_rpg_discord_user["player_name"]}')
        ##contentPage > div > div.vehiclesContainer > div"
        #https://www.rpg.b-zone.ro/players/vehicles/Wikkie
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.rpg.b-zone.ro/players/vehicles/{is_registered_rpg_discord_user["player_name"]}') as resp:
                content = await resp.text()
                doc = BeautifulSoup(content, "html.parser")
                print(len(doc.select('#contentPage > div > div.vehiclesContainer > div')))
                car_select_list = []
                car_embed_list = []
                for i in range(1,len(doc.select('#contentPage > div > div.vehiclesContainer > div'))+1):
                    embed = discord.Embed(
                    title=f'{is_registered_rpg_discord_user["player_name"]}\' Vehicles',
                    description="Here's the list of your vehicles",
                    color=discord.Colour.random()
                    )
                    embed.set_footer(text="use `!help` to know more |use !suggestions to share your ideas",icon_url="https://cdn.discordapp.com/avatars/491251010656927746/6f81dc8d0bc07ff152b244e0958b5961.png?size=1024")
                    embed.add_field(name="Vehicle Model",value=f"{doc.select(f'#contentPage > div > div.vehiclesContainer > div:nth-child({i}) > table > tr:nth-child(1) > td:nth-child(2)')[0].string.strip()}",inline=True)
                    embed.add_field(name="Dealership Price",value=f"{doc.select(f'#contentPage > div > div.vehiclesContainer > div:nth-child({i}) > table > tr:nth-child(2) > td:nth-child(2)')[0].string.strip()}",inline=True)
                    embed.add_field(name="Vehicle Type",value=f"{doc.select(f'#contentPage > div > div.vehiclesContainer > div:nth-child({i}) > table > tr:nth-child(4) > td:nth-child(2)')[0].string.strip()}",inline=True)
                    embed.add_field(name="Vehicle Odometer",value=f"{doc.select(f'#contentPage > div > div.vehiclesContainer > div:nth-child({i}) > table > tr:nth-child(6) > td:nth-child(2)')[0].string.strip()}",inline=True)
                    embed.add_field(name="Vehicle Age",value=f"{doc.select(f'#contentPage > div > div.vehiclesContainer > div:nth-child({i}) > table > tr:nth-child(7) > td:nth-child(2)')[0].string.strip()}",inline=True)
                    embed.add_field(name="Vehicle VIP",value=f"{doc.select(f'#contentPage > div > div.vehiclesContainer > div:nth-child({i}) > table > tr:nth-child(10) > td:nth-child(2)')[0].string.strip()}",inline=True)
                    embed.set_image(url=doc.select(f"#contentPage > div > div.vehiclesContainer > div:nth-child({i}) > div > img")[0]['src'])
                    car_select_list.append(discord.SelectOption(value=i-1,label=f"{doc.select(f'#contentPage > div > div.vehiclesContainer > div:nth-child({i}) > table > tr:nth-child(1) > td:nth-child(2)')[0].string.strip()} - {doc.select(f'#contentPage > div > div.vehiclesContainer > div:nth-child({i}) > table > tr:nth-child(6) > td:nth-child(2)')[0].string.strip()}km",emoji="🚀"))
                    car_embed_list.append(embed)
                view = View(timeout=None)
                sell_button= Button(label="Sell",style=discord.ButtonStyle.danger,emoji="💲",custom_id="generalButton")
                view.add_item(sell_button)
                car_select_menu = Select(options=car_select_list)
                
                async def select_callback(interaction):
                    print(interaction.data["values"][0])
                    await interaction.response.edit_message(embed=car_embed_list[int(interaction.data["values"][0])])
                async def button_callback(interaction):
                    print(interaction.message.embeds[0].fields)
                sell_button.callback = button_callback
                car_select_menu.callback = select_callback
                view.add_item(car_select_menu)
                await ctx.send(embed=car_embed_list[0],view=view)
    else:   
        await ctx.reply("Registered : False")