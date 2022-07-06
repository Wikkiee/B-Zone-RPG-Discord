import aiohttp
import asyncio
from unit_functions import global_url

async def keep_alive():
    print()
    await asyncio.sleep(30)
    async with aiohttp.ClientSession() as session:
                        site_url = f'{global_url}/'
                        async with session.get(site_url) as resp:
                            res =  await resp.json()
                            if(res["status_code"] == 200):
                                print(f'[Keep-Alive] : Ok')
                            else:
                                print(f'[Keep-Alive] : Failed')