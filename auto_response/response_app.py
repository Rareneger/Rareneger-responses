from kivy.app import App
from message import *

class ResponseApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = self.get_url_database()
        self.messager = Messager()

    def responder_button(self):
        self.url = self.root.get_screen('menu').children[0].children[1].children[0].text
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
        self.root.get_screen('respostas').children[0].children[2].text = self.messager.make_message()

if __name__ == '__main__':
    app = ResponseApp()
    app.run()
