import aiohttp
import asyncio

from bs4 import BeautifulSoup

async def get_page(session,url):
    async with session.get(url) as r:
        return await r.text()

async def get_all(session,urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session,url))
        tasks.append(task) 
    result = await asyncio.gather(*tasks)
    return result

async def main(urls):
    print("Called")
    async with aiohttp.ClientSession() as session:
        data = await get_all(session,urls)
        return data

def parse(result):
    for html in result:
        soup = BeautifulSoup(html)
        data = soup.select("#getting-started > h2")
        print(data)


if __name__ == "__main__":

        urls = [
            "https://docs.aiohttp.org/en/stable/",
            "https://pypi.org/project/beautifulsoup4/",
            "https://understandingdata.com/python-for-seo/asynchronous-web-scraping-python/"
        ]

        result = asyncio.run(main(urls))
        parse(result)



































































































































# #------------------------Heroku section -------------------------------


# # from selenium import webdriver
# # import os

# # chrome_options = webdriver.ChromeOptions()
# # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# # chrome_options.add_argument("--headless")
# # chrome_options.add_argument("--disable-dev-shm-usage")
# # chrome_options.add_argument("--no-sandbox")
# # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

# #------------------------Heroku section -------------------------------

# #------------------------local section -------------------------------


# import time
# import traceback
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# #-----------------------Chrome options ---------------------------

# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import InvalidSessionIdException
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# # prefs = {'profile.default_content_setting_values': {'images': 2}}
# # chrome_options.add_experimental_option("prefs", prefs)
# # chrome_options.add_argument("--headless") # Runs Chrome in headless mode.
# # chrome_options.add_argument('--no-sandbox') # Bypass OS security model
# # chrome_options.add_argument('--disable-gpu')  # applicable to windows os only
# # chrome_options.add_argument('start-maximized') # 
# chrome_options.add_argument('disable-infobars')
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-logging")
# chrome_options.add_argument("--disable-login-animations")
# chrome_options.add_argument("--disable-default-apps")
# chrome_options.add_argument("--use-fake-device-for-media-stream")
# chrome_options.add_argument("--use-fake-ui-for-media-stream")

# # chrome_options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])



# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=chrome_options)
# # drivera = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=chrome_options)

# #------------------------local section -----------------------------



# async def get_player_data(player_name,driver):
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=chrome_options)
#     start_time = time.time()
#     try:
#         driver.get(f'https://www.rpg.b-zone.ro/players/general/{player_name}')
#         print(driver.title)
#         # element = driver.find_element(By.CSS_SELECTOR, "#wrapper > div.generalRight > table > tbody > tr.firstRow > td:nth-child(2) > div > div > div > div.tooltipstered > a:nth-child(1)")
#         # print(element.text)
#         isValidPlayerName = driver.find_element(By.CSS_SELECTOR,"#contentPage > div").text
#         if(isValidPlayerName == 'Player not found'):
#             end_time = time.time()
#             total_time = "Total execution time: {} seconds".format(end_time - start_time)
#             return({
#                 "total_time":total_time,
#                 "data":{"playerFound":0,"message":"Player not found"}
#                 })
#         else:
#             name_lenght = len(driver.find_elements(By.CSS_SELECTOR,"#wrapper > div.generalRight > table > tbody > tr.firstRow > td:nth-child(2) > div > div > div > div.tooltipstered > a"))
#             print(name_lenght)
#             validName = name_lenght > 1 and driver.find_element(By.CSS_SELECTOR,"#wrapper > div.generalRight > table > tbody > tr.firstRow > td:nth-child(2) > div > div > div > div.tooltipstered > a:nth-child(1)").text+driver.find_element(By.CSS_SELECTOR,"#wrapper > div.generalRight > table > tbody > tr.firstRow > td:nth-child(2) > div > div > div > div.tooltipstered > a:nth-child(2)").text or driver.find_element(By.CSS_SELECTOR,"#wrapper > div.generalRight > table > tbody > tr.firstRow > td:nth-child(2) > div > div > div > div.tooltipstered > a:nth-child(1)").text
#             print(validName)
#             data = {
#                         "ign": validName,
#                         "profile_url":f'https://www.rpg.b-zone.ro/players/general/{player_name}',
#                         "avatar_url":driver.find_element(By.CSS_SELECTOR,".skinImg ").get_attribute("src"),
#                         "current_status":driver.find_element(By.CSS_SELECTOR,"#wrapper > div.generalRight > table > tbody > tr.firstRow > td:nth-child(2) > div > div > div > div:nth-child(1) > img").get_attribute("alt"),
#                         "level":driver.find_element(By.CSS_SELECTOR,"#generalTableLeft > table > tbody > tr:nth-child(3) > td:nth-child(2)").text,
#                         "last_login":driver.find_element(By.CSS_SELECTOR,"#wrapper > div.generalRight > table > tbody > tr:nth-child(3) > td:nth-child(2)").text,
#                         "hours_played_this_month":driver.find_element(By.CSS_SELECTOR,"#generalTableLeft > table > tbody > tr:nth-child(6) > td:nth-child(2)").text,
#                         "real_hours_this_month":driver.find_element(By.CSS_SELECTOR,"#generalTableLeft > table > tbody > tr:nth-child(7) > td:nth-child(2)").text,
#                         "respect":driver.find_element(By.CSS_SELECTOR,"#generalTableLeft > table > tbody > tr:nth-child(4) > td:nth-child(2)").text,
#                         "hours_played":driver.find_element(By.CSS_SELECTOR,"#generalTableLeft > table > tbody > tr:nth-child(5) > td:nth-child(2)").text,
#                         "married":driver.find_element(By.CSS_SELECTOR,"#generalTableRight > table > tbody > tr.firstRow > td:nth-child(2)").text,
#                         "driving_lic":driver.find_elements(By.CSS_SELECTOR,"#licText")[0].text,
#                         "flying_lic":driver.find_elements(By.CSS_SELECTOR,"#licText")[1].text,
#                         "sailing_lic":driver.find_elements(By.CSS_SELECTOR,"#licText")[2].text,
#                         "fishing_lic":driver.find_elements(By.CSS_SELECTOR,"#licText")[3].text,
#                         "weapon_lic":driver.find_elements(By.CSS_SELECTOR,"#licText")[4].text,
#                         "materials_lic":driver.find_elements(By.CSS_SELECTOR,"#licText")[5].text,
#                         "playerFound":1,
#                         "message":0
#              }
#             driver.get(f'https://www.rpg.b-zone.ro/players/faction/{player_name}')
#             faction_data = {
#                         "faction_name": driver.find_element(By.CSS_SELECTOR,"#FactionWrapper > table > tbody > tr:nth-child(1) > td:nth-child(2)").text,
#                         "join_date": driver.find_element(By.CSS_SELECTOR,"#FactionWrapper > table > tbody > tr:nth-child(2) > td:nth-child(2)").text,
#                         "rank": driver.find_element(By.CSS_SELECTOR,"#FactionWrapper > table > tbody > tr:nth-child(3) > td:nth-child(2)").text,
#                         "faction_warns": driver.find_element(By.CSS_SELECTOR,"#FactionWrapper > table > tbody > tr:nth-child(4) > td:nth-child(2)").text,
#                         "faction_punish": driver.find_element(By.CSS_SELECTOR,"#FactionWrapper > table > tbody > tr:nth-child(5) > td:nth-child(2)").text,
#                         "faction_time": driver.find_element(By.CSS_SELECTOR,"#FactionWrapper > table > tbody > tr:nth-child(6) > td:nth-child(2)").text,
#                         "faction_url" : (driver.find_element(By.CSS_SELECTOR,"#FactionWrapper > table > tbody > tr:nth-child(1) > td:nth-child(2)").text != 'Civilian') and driver.find_element(By.CSS_SELECTOR,"#FactionWrapper > table > tbody > tr.firstRow > td:nth-child(2) > a").get_attribute("href") or None,
#                     }
            
#             data.update(faction_data)
#             if((driver.find_element(By.CSS_SELECTOR,"#FactionWrapper > table > tbody > tr:nth-child(1) > td:nth-child(2)").text != 'Civilian')):
#                 driver.get(data["faction_url"])
#                 data.update({
#                     "faction_logo_url":driver.find_element(By.CSS_SELECTOR,"#pageContent > p:nth-child(3) > img").get_attribute("src")
                    
#                 })
#             else:
#                 print("Player is civilian") 
#             print('\n ======> Final Data <====== : \n')
#             print(data)
#             end_time = time.time()
#             total_time = "Total execution time: {} seconds".format(end_time - start_time)
#             driver.close()
#             return({
#                 "total_time":total_time,
#                 "data":data
#             })
    

    
    
#     except Exception as e:
#         print(traceback.format_exc())
#         print("Errors_2")
#         print(e.__class__)




























































































