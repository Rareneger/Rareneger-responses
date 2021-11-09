from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

class WhatsappSender():
    def __init__(self):
        self.options = Options()
        self.options.add_argument("user-data-dir=chrome-user-data")

    def send_message(self, message, number, progress, rate=1):
        url = f'https://web.whatsapp.com/send?phone={number}&text={message}'
        with webdriver.Chrome(chrome_options=self.options) as driver:
            driver.get(url)
            driver.minimize_window()
            while len(driver.find_elements(by='id', value='side')) < 1:
                sleep(1)
            progress.update(2 / rate)
            sleep(5)
            progress.update(4 / rate)
            driver.find_element(by='xpath', value='//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]').send_keys(Keys.ENTER)
            sleep(5)
            progress.update(4 / rate)

    def do_login(self):
        with webdriver.Chrome(chrome_options=self.options) as driver:
            driver.get('https://web.whatsapp.com')

            while len(driver.find_elements(by='id', value='side')) < 1:
                sleep(1)
