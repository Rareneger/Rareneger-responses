# -*- coding: utf-8 -*-

from numpy import isnan
import pandas as pd
import json
from infos import Info


class Messager():
    def __init__(self):
        self.info = Info()
        self.form_df = self.read_df()
        self.actual_row = self.read_timestamp()
        self.pay_codes = self.info.get_pay_codes()

    def read_timestamp(self):
        actual_row = 0
        last_timestamp = self.info.get_last_timestamp()
        if last_timestamp :
                for i, timestamp in enumerate(self.form_df['Timestamp']):
                    if timestamp == last_timestamp:
                        actual_row = i + 1
                        break
        return actual_row

    def read_df(self):
        try:
            return pd.read_csv(self.info.get_url_form())
        except OSError:
            print('something failure opening your url')
            return None

    def _update_row(self): 
        self.actual_row += 1

    def make_message(self):
        if self.actual_row < len(self.form_df):
            name = self.form_df['Nome:'][self.actual_row]
            contact_way = self.form_df['Por onde deseja receber as informações de confirmação do atendimento?'][self.actual_row]
            contact_number = None
            
            if 'Whatsapp' in contact_way:
                num = self.form_df['Para receber por Whatsapp informe o número de celular:'][self.actual_row]
                if not isnan(num):
                    contact_number = '55' + str(int(num))
            
            if 'Email' in contact_way:
                contact_email = self.form_df['Para receber por Email informe o Email:'][self.actual_row]
            else:
                contact_email = None
            alternative_payment = ''

            if 'Presencial' in self.form_df['Modalidade'][self.actual_row]:
                alternative_payment = 'ou presencialmente após o atendimento'

            attendance_kind = self.form_df['Atendimento'][self.actual_row].split('-')[0].strip()
            schedule_possibilities = f'{self.form_df["Início"][self.actual_row]} e {self.form_df["Fim"][self.actual_row]}'

            print(f'Marque uma \033[1;32m{attendance_kind}\033[m, a pessoa está disponível entre \033[1;33m{schedule_possibilities}\033[m nos dias \033[1;33m{self.form_df["Disponibilidade de dias da semana"][self.actual_row]}\033[m')

            mark_date = input('digite a data: ')

            mark_schedule = input('digite o hórario: ')

            text_message = f'Olá {name}, tudo bem? aqui é o Rareneger\n \nA sua {attendance_kind} está marcada para {mark_date} as {mark_schedule}.\nGratidão por se permitir\n \nVocê pode realizar o pagamento pelo pix {alternative_payment}\n \nEsta é uma mensagem automática de confirmação, segue o código para o pix copia e cola.\n \n'

            pay_message = self.pay_codes[attendance_kind]

            message = (text_message, pay_message)
            
            print('')
            print('A mensagem a ser enviada será: ')
            print('\033[33m-=-\033[m' * 15)
            print(text_message)
            print(pay_message)
            print('\033[33m-=-\033[m' * 15)

            if not contact_number and not contact_email:
                print('\033[31m* A pessoa não disponibilizou meios de contato\033[m')

            self._update_row()

            return message, contact_email, contact_number
        else:
            return None

    def on_exit(self):
        last_timestamp = self.form_df['Timestamp'][self.actual_row - 1]
        self.info.set_last_timestamp(last_timestamp)

    def back_row(self):
        if self.actual_row > 0:
            self.actual_row -= 1
