from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#-----------------------Chrome options ---------------------------

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
#chrome_options.add_argument("--headless") # Runs Chrome in headless mode.
#chrome_options.add_argument('--no-sandbox') # Bypass OS security model
#chrome_options.add_argument('--disable-gpu')  # applicable to windows os only
# chrome_options.add_argument('start-maximized') # 
# chrome_options.add_argument('disable-infobars')
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--disable-logging")
# chrome_options.add_argument("--disable-login-animations")
# chrome_options.add_argument("--disable-default-apps")
# chrome_options.add_argument("--use-fake-device-for-media-stream")
# chrome_options.add_argument("--use-fake-ui-for-media-stream")
# chrome_options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])

#-----------------------Chrome options ---------------------------

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=chrome_options)

async def scrapper():
    print("Test")