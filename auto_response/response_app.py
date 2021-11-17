from kivy.app import App
from kivy.metrics import sp
from kivy.uix.label import Label
from message import Messager
from send import EmailSender
from infos import Info
from googleapiclient.errors import HttpError

class ResponseApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_person = None
        self.infos = None
        self.messager = None
        self.email_sender = None

    def responder_button(self):
        try:
            if not self.infos:
                self.infos = Info(self.root.ids.id_input.text)
                self.messager = Messager(self.infos)
                self.email_sender = EmailSender(self.infos)
            self.update_screen()
        except HttpError:
            self.root.ids.id_error_message.text = 'O id informado não é válido'

    def enviar_mensagem_button(self):
        self.root.current = 'loading'

    def send_message(self):
        self.current_person.date = self.root.ids.date_input.text
        self.current_person.time = self.root.ids.time_input.text
        message = self.messager.mount_message(self.current_person)
        pay_code = self.infos.get_pay_codes()[self.current_person.attendance_kind]
        
        self.email_sender.send_email(f'{message}{pay_code}',
        self.current_person.email)
        self.update_row()
        self.update_screen()

    def update_row(self):
        self.messager.update_timestamp()
        self.messager.next_row()

    def update_screen(self):
        if self.messager.is_position_valid():
            self.current_person = self.messager.get_person_infos()
            self.root.ids.command_message.text = \
                self.messager.get_command_message(self.current_person)
            self.root.current = 'respostas'
        else:
            self.root.current = 'end'


class Message(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)

    def on_size(self, *args):
        self.text_size = (self.width - sp(10), None)

    def on_texture_size(self, *args):
        self.size = self.texture_size
        self.height += sp(20)

if __name__ == '__main__':
    app = ResponseApp()
    app.run()
