from numpy import empty
import pandas as pd


class Messager():
    def __init__(self):
        try:
            with open('personal-infos/url_form.txt', 'r') as file:
                url = file.read()
        except FileNotFoundError:
            print('the url file was not find')

        try:
            self.form_df = pd.read_csv(url)
        except OSError:
            print('something failure opening your url')
        self.last_timestamp = None
        self.actual_row = None
        self._update_row()
    
    def _update_row(self):        
        try:
            with open('personal-infos/last_timestamp.txt', 'r') as file:
                self.last_timestamp = file.read()
        except FileNotFoundError:
            print('the timestamp file was not find')

        self.actual_row = 0
        if self.last_timestamp:
            for i, timestamp in enumerate(self.form_df['Timestamp ']):
                if timestamp == self.last_timestamp:
                    self.actual_row = i + 1
                    break
        
        if self.actual_row < len(self.form_df):
            last_timestamp = self.form_df['Timestamp '][self.actual_row]
            try:
                with open('personal-infos/last_timestamp.txt', 'w') as file:
                    file.write(last_timestamp)
            except FileNotFoundError:
                print('the timestamp file was not find')

    def make_message(self):

        if self.actual_row < len(self.form_df):
            name = self.form_df['Nome: '][self.actual_row]
            contact_way = self.form_df['Por onde deseja receber as informações de confirmação do atendimento? '][self.actual_row]
            
            if 'Whatsapp' in contact_way:
                contact_number = '55' + self.form_df['Para receber por Whatsapp informe o número de celular: '][self.actual_row]
            else:
                contact_number = None

            if 'Email' in contact_way:
                contact_email = self.form_df['Para receber por Email informe o Email: '][self.actual_row]
            else:
                contact_email = None

            attendance_kind = self.form_df['Atendimento '][self.actual_row].split('-')[0].strip()
            schedule_possibilities = f'{self.form_df["Início "][self.actual_row]} e {self.form_df["Fim "][self.actual_row]}'

            print(f'Marque uma {attendance_kind}, a pessoa está disponível entre {schedule_possibilities} nos dias {self.form_df["Disponibilidade de dias da semana "][self.actual_row]}')

            mark_date = input('digite a data: ')

            mark_schedule = input('digite o hórario: ')

            print('A menssagem a ser enviada será: ')
            messagem = f'Olá {name}, tudo bem? aqui é o Rareneger \nA sua {attendance_kind} está marcada para {mark_date} as {mark_schedule}.' 
            print(messagem)
            self._update_row()
            return messagem, contact_email, contact_number
        else:
            return None

    def return_row(self):
        self._update_row()
        self.actual_row -= 1
