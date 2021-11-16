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
        if last_timestamp :
                for i, timestamp in enumerate(self.form_df['Timestamp']):
                    if timestamp == last_timestamp:
                        actual_row = i + 1
                        break
        return actual_row

    def _update_row(self): 
        self.actual_row += 1

    def make_message(self):
        if self.actual_row < len(self.form_df):
            
            attendance_kind = self.form_df['Atendimento'][self.actual_row].split('-')[0].strip()
            schedule_possibilities = f'{self.form_df["Início"][self.actual_row]} e {self.form_df["Fim"][self.actual_row]}'

            command_message = f'Marque uma {attendance_kind}, a pessoa está disponível entre {schedule_possibilities} nos dias {self.form_df["Disponibilidade de dias da semana"][self.actual_row]}'

            return command_message
        else:
            return ''

    def on_exit(self):
        last_timestamp = self.form_df['Timestamp'][self.actual_row - 1]
        self.info.set_last_timestamp(last_timestamp)

    def back_row(self):
        if self.actual_row > 0:
            self.actual_row -= 1

class Person():
    def __init__(self, phone, email, name, attendance_kind):
        self.phone = phone
        self.email = email
        self.name = name
        self.attendance_kind = attendance_kind
        self.date
        self.time

    def set_date_time(self, date, time):
        self.date = date
        self.time = time