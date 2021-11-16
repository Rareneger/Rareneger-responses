# -*- coding: utf-8 -*-
from infos import Info


class Messager():
    def __init__(self):
        self.info = Info()
        self.form_df = self.info.get_form_df()
        self.actual_row = self.read_timestamp()
        self.pay_codes = self.info.get_pay_codes()

    def read_timestamp(self):
        actual_row = 0
        last_timestamp = self.info.get_last_timestamp()
        if last_timestamp:
                for i, timestamp in enumerate(self.form_df['Carimbo de data/hora']):
                    if timestamp == last_timestamp:
                        actual_row = i + 1
                        break
        return actual_row

    def _update_row(self): 
        self.actual_row += 1

    def get_command_message(self, person):
        if self.actual_row < len(self.form_df):
            command_message = f'Marque uma {person.attendance_kind}, a pessoa está disponível entre {person.schedule_possibilities} nos dias {person.days_possibilities}'

            return command_message
        else:
            return ''

    def get_person_infos(self):
        email = self.form_df['Para receber a confirmação por Email, informe o Email:'][self.actual_row]
        name = self.form_df['Nome:'][self.actual_row]
        attendance_kind = self.form_df['Atendimento'][self.actual_row].split('-')[0].strip()
        schedule_possibilities = f'{self.form_df["Início"][self.actual_row]} e {self.form_df["Fim"][self.actual_row]}'
        days_possibilities = self.form_df['Disponibilidade de dias da semana'][self.actual_row]
        modality = self.form_df['Modalidade'][self.actual_row]
        return PersonInfos(email, name, attendance_kind, schedule_possibilities, days_possibilities, modality)

    def on_exit(self):
        last_timestamp = self.form_df['Timestamp'][self.actual_row - 1]
        self.info.set_last_timestamp(last_timestamp)

    def back_row(self):
        if self.actual_row > 0:
            self.actual_row -= 1

class PersonInfos():
    def __init__(self, email, name, attendance_kind, schedule_possibilities, days_possibilities, modality):
        self.email = email
        self.name = name
        self.attendance_kind = attendance_kind
        self.schedule_possibilities = schedule_possibilities
        self.days_possibilities = days_possibilities
        self.modality = modality
        self.date
        self.time

    def set_date_time(self, date, time):
        self.date = date
        self.time = time