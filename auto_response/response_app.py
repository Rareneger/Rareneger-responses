from kivy.app import App

class ResponseApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = self.get_url_database()

    def responder_button(self):
        self.url = self.root.get_screen('menu').children[0].children[1].children[0].text
        self.set_url_database()
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

if __name__ == '__main__':
    app = ResponseApp()
    app.run()
