
import asyncio
import os
import aiohttp
import time
async def imgur_hanlder(image_url_list):
    start_time = time.time()
    print("[Imgur Task] : Task started")
    API_ENDPOINT = "https://api.imgur.com/3"
    headers = {
        "Authorization":f'Client-ID {os.environ.get("CLIENT_ID")}'
    }
    data = {
        "privacy":"hidden"
    }
    
    
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url = f'{API_ENDPOINT}/album', data = data,headers=headers) as resp:
            res = await resp.json()
            album_id = res["data"]["id"]
            album_delete_hash_id = res["data"]["deletehash"]

            uploaded_images_id = []
            uploaded_images_deletehash_id = []
            uploaded_images_link = []
            async def upload_mulitple(image_post_data):
                async with session.post(url= f'{API_ENDPOINT}/upload',data=image_post_data,headers=headers) as resp:
                        res = await resp.json()
                        uploaded_images_link.append(res["data"]["link"])
                        uploaded_images_id.append(res["data"]["id"])
                        uploaded_images_deletehash_id.append(res["data"]["deletehash"])
            tasks = []
            for image in image_url_list:
                image_post_data = {
                    "image":image.url,
                    "type":"url",
                }
                task = asyncio.create_task(upload_mulitple(image_post_data))
                tasks.append(task)
            
            await asyncio.gather(*tasks)

            #https://api.imgur.com/3/
            album_image_add_data = {
                "deletehashes[]":uploaded_images_deletehash_id
                }
            async with session.post(url= f'{API_ENDPOINT}/album/{album_delete_hash_id}/add',data=album_image_add_data,headers=headers) as resp:
                    res = await resp.json()
                                
            #https://api.imgur.com/3/album/{{albumHash}}
            async with session.get(url= f'{API_ENDPOINT}/album/{album_id}',headers=headers) as resp:
                    res = await resp.json()
                    print("[Imgur Task] : Task completed ... Sending the link")
                    end_time = time.time()
                    total_time = "Result in : {} seconds".format(int(end_time - start_time)) 
                    print(total_time)
                    album_link = {
                        "first_image_link":uploaded_images_link[0],
                        "album_post_link":res["data"]["link"],
                        "time_taken":total_time
                    }

                    return album_link


























































# API_ENDPOINT = "https://api.imgur.com/3"
#     headers = {
#         "Authorization":f'Client-ID {os.environ.get("CLIENT_ID")}'
#     }
#     data = {
#         "privacy":"hidden"
#     }
#     r = requests.post(url = f'{API_ENDPOINT}/album', data = data,headers=headers) 
#     res = r.json()
#     album_id = res["data"]["id"]
#     album_delete_hash_id = res["data"]["deletehash"]

#     uploaded_images_id = []
#     uploaded_images_deletehash_id = []
#     uploaded_images_link = []
#     for image in image_url_list:
#         image_post_data = {
#             "image":image.url,
#             "type":"url",
#         }
#         r = requests.post(url= f'{API_ENDPOINT}/upload',data=image_post_data,headers=headers)
#         res = r.json()
#         uploaded_images_link.append(res["data"]["link"])
#         uploaded_images_id.append(res["data"]["id"])
#         uploaded_images_deletehash_id.append(res["data"]["deletehash"])


#     #https://api.imgur.com/3/
#     album_image_add_data = {
#         "deletehashes[]":uploaded_images_deletehash_id
#     }
#     r = requests.post(url= f'{API_ENDPOINT}/album/{album_delete_hash_id}/add',data=album_image_add_data,headers=headers)
#     res = r.json()


#     #https://api.imgur.com/3/album/{{albumHash}}

#     r = requests.get(url= f'{API_ENDPOINT}/album/{album_id}',headers=headers)
#     res = r.json()
#     print("\n Album links \n")
#     album_link = {
#         "first_image_link":uploaded_images_link[0],
#         "album_post_link":res["data"]["link"]
#         }


#     return album_link























    # print(image_data)
    # client_id = os.environ.get("CLIENT_ID")
    # client_secret = os.environ.get("CLIENT_SECRET")
    # client = ImgurClient(client_id, client_secret)
    # # print(client.get_auth_url('pin')) #go to page and copy down pin
    # # creds = client.authorize(input('Pin: '), 'pin')
    # # print(creds['refresh_token'])
    # # client.set_user_auth(creds['access_token'], creds['refresh_token'])
    
    # # client.set_user_auth(access_token, refresh_token)
    # uploaded_image_links = []
    # uploaded_image_ids = []
    # uploaded_image_deletehashid = []
    # albumspec = {
    # 'title': 'B-zone Discord Bot',
    # 'privacy': 'hidden'
    # }

    # albumdata = client.create_album(albumspec)
    # print(albumdata)
    
    # for item in image_data:
    #     upload_result = client.upload_from_url(item.url, config={'album':None}, anon=True)
    #     print(upload_result["id"])
    #     print(upload_result)
    #     uploaded_image_links.append(upload_result["link"])
    #     uploaded_image_ids.append(upload_result["id"])
    #     uploaded_image_deletehashid.append(upload_result["deletehash"])

    # print("\n ")
    # print(uploaded_image_ids)
    # print("\nAlbum data\n")
    
    # # client.album_add_images()
    # # album_upload_result = client.album_add_images(,uploaded_image_deletehashid)
    # return uploaded_image_links
    