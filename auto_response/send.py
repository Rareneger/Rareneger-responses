# -*- coding: utf-8 -*-

import smtplib
import email.message


class EmailSender():
    def __init__(self, infos):
        self.infos = infos
        self.email, self.password = self.get_email()

    def get_email(self):
        return self.infos.get_email(), self.infos.get_email_password()

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
