from kivy.app import App
from kivy.metrics import sp
from kivy.uix.label import Label
from message import *
from send import *

class ResponseApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = self.get_url_database()
        self.messager = Messager()
        self.email_sender = EmailSender()

    def responder_button(self):
        self.url = self.root.ids.url_input.text
        self.set_url_database()
        self.get_message_command()
        self.root.current = 'respostas'

    def set_url_database(self):
        with open('auto_response/personal-infos/data-url.txt', 'w', encoding='utf-8') as file:
            file.write(self.url)

    def get_url_database(self):
        try:
            with open('auto_response/personal-infos/data-url.txt', 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return ''

    def get_message_command(self):
        self.root.ids.command_message.text = self.messager.make_message()


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
