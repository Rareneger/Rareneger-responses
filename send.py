# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from urllib import parse
import smtplib
import email.message

class WhatsappSender():
    def __init__(self):
        self.options = Options()
        self.options.add_argument("user-data-dir=chrome-user-data")

    def send_message(self, message, number, progress, rate=1):
        url_message = parse.quote(message)
        url = f'https://web.whatsapp.com/send?phone={number}&text={url_message}'
        try:
            with webdriver.Chrome(chrome_options=self.options) as driver:
                driver.get(url)
                driver.minimize_window()
                while len(driver.find_elements(by='id', value='side')) < 1:
                    sleep(1)
                progress.update(2 / rate)
                sleep(5)
                progress.update(4 / rate)
                driver.find_element(by='xpath', value='/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]').send_keys(Keys.ENTER)
                sleep(5)
                progress.update(4 / rate)
        except exceptions.WebDriverException:
            print(f'algo deu errado enviando a mensagem para {number}')
            print('')
            print(message)
            input('Precione Enter para continuar')

    def do_login(self):
        with webdriver.Chrome(chrome_options=self.options) as driver:
            driver.get('https://web.whatsapp.com')

            while len(driver.find_elements(by='id', value='side')) < 1:
                sleep(1)

class EmailSender():
    def __init__(self):
        self.email, self.password = self.get_email()

    def get_email(self):
        try:
            with open('personal-infos/email.txt', 'r') as file:
                email = file.read()
        except FileNotFoundError:
            email = None
            print('o arquivo de email não foi encontrado')

        try:
            with open('personal-infos/email-password.txt', 'r') as file:
                password = file.read()
        except FileNotFoundError:
            password = None
            print('o arquivo de email não foi encontrado')

        return email, password

    def send_email(self, text, email_to):
        msg = email.message.Message()
        msg['Subject'] = 'Confirmação de atendimento Rareneger'
        msg['From'] = self.email
        msg['To'] = email_to
        msg.add_header('Content-type', 'text/html')
        msg.set_payload(self._html_conversion(text))

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], self.password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

    def _html_conversion(self, text):
        lines = text.split('\n')
        html_message = ''
        for line in lines:
            html_message = html_message + '<p>' + line + '</p> \n'
        return html_message