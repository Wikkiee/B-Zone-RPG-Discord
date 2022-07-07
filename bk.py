        # time.sleep(8)
        # async with aiohttp.ClientSession() as session:
        #     site_url = f'https://www.rpg.b-zone.ro/players/general/{player_name}'
        #     async with session.get(site_url) as resp:
        #         content = await resp.text()
        #         soup = BeautifulSoup(content, 'html.parser')
        #         print(soup.find_all("div",class_="tooltipstered"))
                # await playerinfo_command.playerinfo_func(discord,ctx,data)
        # time.sleep(8)
        # async with aiohttp.ClientSession() as session:
        #     site_url = f'{global_url}/playerinfo/{player_name}'
        #     async with session.get(site_url) as resp:
        #         data = await resp.json()
        #         await playerinfo_command.playerinfo_func(discord,ctx,data)





        



#@client.command(aliases = ["termi"] )
# async def terminate(ctx, password):
#     print
#     if int(password) == 123:
#         await ctx.reply("Terminating...")
#         await client.close()
#     else:
#         await ctx.reply("please enter the valid password")

























    # async with aiohttp.ClientSession() as session:
    #     async with session.get(f'https://www.rpg.b-zone.ro/players/general/{player_name}') as resp:
    #         content = await resp.text()
    #         doc = BeautifulSoup(content, 'html.parser')
    #         rpg_player_ign = doc.select(".tooltipstered a")
    #         print(len(rpg_player_ign))
    #         if(len(rpg_player_ign)>0):
    #             full_name =len(rpg_player_ign) > 1 and f'{rpg_player_ign[0].string}{rpg_player_ign[1].string}' or rpg_player_ign[0].string
    #             print("player found")            
    #             data = {
    #                     "ign": full_name,
    #                     "profile_url":f'https://www.rpg.b-zone.ro/players/general/{player_name}',
    #                     "avatar_url": doc.select(".skinImg")[0]["src"],
    #                     "current_status": doc.select("#wrapper > div.generalRight > table > tr.firstRow > td:nth-child(2) > div > div > div > div:nth-child(1) > img")[0]["alt"],
    #                     "level":doc.select("#generalTableLeft > table > tr:nth-child(3) > td:nth-child(2)")[0].string.strip(),
    #                     "last_login":doc.select("#wrapper > div.generalRight > table > tr:nth-child(3) > td:nth-child(2)")[0].string.strip(),
    #                     "hours_played_this_month":doc.select("#generalTableLeft > table > tr:nth-child(6) > td:nth-child(2)")[0].string.strip(),
    #                     "real_hours_this_month":doc.select("#generalTableLeft > table > tr:nth-child(7) > td:nth-child(2)")[0].string.strip(),
    #                     "respect":doc.select("#generalTableLeft > table > tr:nth-child(4) > td:nth-child(2)")[0].string.strip(),
    #                     "hours_played":doc.select("#generalTableLeft > table > tr:nth-child(5) > td:nth-child(2)")[0].string.strip(),
    #                     "married":doc.select("#generalTableRight > table > tr.firstRow > td:nth-child(2)")[0].string.strip(),
    #                     "playerFound":1,
    #                     "message":0
                                           
    #                     }
    #             async with session.get(f'https://www.rpg.b-zone.ro/players/faction/{player_name}') as resp:
    #                 content = await resp.text()
    #                 doc = BeautifulSoup(content, 'html.parser')
    #                 faction_name = (doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].a == None) and doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].string.strip() or doc.select("#FactionWrapper > table > tr:nth-child(1) > td:nth-child(2)")[0].a.string.strip()
    #                 faction_data = {
    #                     "faction_name":faction_name,
    #                     "join_date": doc.select("#FactionWrapper > table > tr:nth-child(2) > td:nth-child(2)")[0].string.strip(),
    #                     "rank": doc.select("#FactionWrapper > table > tr:nth-child(3) > td:nth-child(2)")[0].string.strip(),
    #                     "faction_warns": doc.select("#FactionWrapper > table > tr:nth-child(4) > td:nth-child(2)")[0].string.strip(),
    #                     "faction_punish": doc.select("#FactionWrapper > table > tr:nth-child(5) > td:nth-child(2)")[0].string.strip(),
    #                     "faction_time": doc.select("#FactionWrapper > table > tr:nth-child(6) > td:nth-child(2)")[0].string.strip(),
    #                     "faction_url" : (faction_name != 'Civilian') and doc.select("#FactionWrapper > table > tr.firstRow > td:nth-child(2) > a")[0]["href"] or None,
    #                         }
    #                 data.update(faction_data)
    #                 if(faction_name != 'Civilian'):
    #                     async with session.get(f'https://www.rpg.b-zone.ro/{data["faction_url"]}') as resp:
    #                         content = await resp.text()
    #                         doc = BeautifulSoup(content, 'html.parser')
    #                         data.update({
    #                             "faction_logo_url":doc.select("#pageContent > p:nth-child(3) > img")[0]["src"]
    #                         })
    #                 else:
    #                     print("Player is civilian")
    #                 print('\n ======> Final Data <====== : \n')
    #                 print(data)
    #                 end_time = time.time()
    #                 total_time = "Total execution time: {} seconds".format(end_time - start_time) 
    #                 print(total_time)
    #         else:
    #             print("player not found")