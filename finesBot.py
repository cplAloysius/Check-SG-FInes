from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import telebot
import json

class checkFinesBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
        chrome_options.add_argument("--window-size=1920,1080")  # Set a specific window size (optional)
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (useful for certain environments)
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems in Docker

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    def setup(self):
        self.driver.get('https://e-station.axs.com.sg')
        self.driver.find_element(by=By.XPATH, value='/html/body/div[3]/table[1]/tbody/tr[2]/td[3]/a').click()
        self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/a[1]').click()
        self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[3]/div[1]/a').click()
        self.driver.find_element(by=By.XPATH, value='//*[@id="inpVehicleNo"]').send_keys(plate_no)

    def check(self):
        tel_bot = telebot.TeleBot(token)
        while True:
            sleep(int(interval))

            self.driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[2]/div[2]/div[2]').click()  
            self.driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[3]/div[1]/a').click()

            while (self.driver.find_element(by=By.XPATH, value='//*[@id="progressDialog_container"]').get_attribute("style") == 'display: block;'):
                continue

            try:
                message = self.driver.find_element(by=By.XPATH, value='//*[@id="spanErrorInpVehicleNo"]').text
                if (message == "No records found. Please try to retrieve by the respective Fines Agency for more details."):
                    continue
                else:
                    tel_bot.send_message(chat_id,"you kena fine")
            
            except NoSuchElementException:
                print("Element not found")
                tel_bot.send_message(chat_id,"you maybe kena fine")

with open('config.json', 'r') as f:
	config = json.load(f)

plate_no = config.get('plate_no')
interval = config.get('interval')
chat_id = config.get('chat_id')
token = config.get('token')

bot = checkFinesBot()
bot.setup()
bot.check()