# -*- coding: utf-8 -*-

import json
import sys

class Configurator():
    def set_email(self):
        the_email = input('digite o email: ')
        with open('personal-infos/email.txt', 'w', encoding='utf-8') as file:
            file.write(the_email)

    def set_email_password(self):
        the_password = input('digite a senha: ')
        with open('personal-infos/email-password.txt', 'w', encoding='utf-8') as file:
            file.write(the_password)

    def set_pay_codes(self):
        consulta_code = input('digite o códico pix para Consulta: ')
        mentoria_code = input('digite o código pix para Mentoria: ')
        tarot_code = input('digite o código pix para Leitura de Tarot: ')
        radeiestesia_code = input('digite o código pix para Radiestesia: ')
        data = {
            'Consulta': consulta_code,
            'Mentoria': mentoria_code,
            'Leitura de Tarot': tarot_code,
            'Radiestesia': radeiestesia_code
        }
        with open('personal-infos/pay-codes.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))

    def set_url_form(self):
        the_url = input('digite a url: ')
        with open('personal-infos/url_form.txt', 'w', encoding='utf-8') as file:
            file.write(the_url)

    def set_last_timestamp(self):
        the_last_timestamp = input('digite o timestamp: ')
        with open('personal-infos/last_timestamp.txt', 'w', encoding='utf-8') as file:
            file.write(the_last_timestamp)

if __name__ == '__main__':
    config = Configurator()
    for arg in sys.argv:
        if arg == 'email':
            config.set_email()
            config.set_email_password()
            print('')
        if arg == 'pix':
            config.set_pay_codes()
            print('')
        if arg == 'url':
            config.set_url_form()
            print('')
        if arg == 'timestamp':
            config.set_last_timestamp()
            print('')