from numpy import isnan
import pandas as pd
import json


class Messager():
    def __init__(self):
        self.form_df = self.read_df()
        self.actual_row = self.read_timestamp()
        self.pay_codes = self.read_pay_codes()

    def read_timestamp(self):
        actual_row = 0
        try:
            with open('personal-infos/last_timestamp.txt', 'r') as file:
                last_timestamp = file.read()
        except FileNotFoundError:
            print('the timestamp file was not find')
            return actual_row
        
        if last_timestamp :
                for i, timestamp in enumerate(self.form_df['Timestamp']):
                    if timestamp == last_timestamp:
                        actual_row = i + 1
                        break
        return actual_row

    def read_df(self):
        try:
            with open('personal-infos/url_form.txt', 'r') as file:
                url = file.read()
        except FileNotFoundError:
            print('the url file was not find')

        try:
            return pd.read_csv(url)
        except OSError:
            print('something failure opening your url')
            return None

    def read_pay_codes(self):
        try:
            with open('personal-infos/pay-codes.json', 'r', encoding='utf8') as file:
                return json.load(file)
        except FileNotFoundError:
            print('the pay-codes file was not find')
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

            attendance_kind = self.form_df['Atendimento'][self.actual_row].split('-')[0].strip()
            schedule_possibilities = f'{self.form_df["Início"][self.actual_row]} e {self.form_df["Fim"][self.actual_row]}'

            print(f'Marque uma {attendance_kind}, a pessoa está disponível entre {schedule_possibilities} nos dias {self.form_df["Disponibilidade de dias da semana"][self.actual_row]}')

            mark_date = input('digite a data: ')

            mark_schedule = input('digite o hórario: ')

            print('')
            print('A menssagem a ser enviada será: ')
            messagem = f'Olá {name}, tudo bem? aqui é o Rareneger\n \nA sua {attendance_kind} está marcada para {mark_date} as {mark_schedule}.\nVocê pode realizar o pagamento pelo pix copia e cola: \n \n{self.pay_codes[attendance_kind]}\n \nGratidão por se permitir\n \nEsta é uma menssagem automática de confirmação.' 
            print(messagem)
            self._update_row()
            return messagem, contact_email, contact_number
        else:
            return None

    def on_exit(self):
        last_timestamp = self.form_df['Timestamp'][self.actual_row - 1]
        try:
            with open('personal-infos/last_timestamp.txt', 'w') as file:
                file.write(last_timestamp)
        except FileNotFoundError:
            print('the timestamp file was not find')

    def back_row(self):
        if self.actual_row > 0:
            self.actual_row -= 1
