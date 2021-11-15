import requests

class Info():
    def __init__(self):
        self.url = self._get_url_database()

    def set_url_database(self, url):
        with open('personal-infos/data-url.txt', 'w') as file:
            file.write(url)

    def _get_url_database(self):
        try:
            with open('personal-infos/data-url.txt', 'r') as file:
                return file.read()
        except FileNotFoundError:
            print('o arquivo da url não foi encontrado')

    def get_url_form(self):
        response = requests.get(self.url + '/form/url.json')
        return response.json()

    def get_email(self):
        response = requests.get(self.url + '/email/email.json')
        return response.json()

    def get_email_password(self):
        response = requests.get(self.url + '/email/password.json')
        return response.json()

    def get_pay_codes(self):
        response = requests.get(self.url + '/pay%20codes.json')
        return response.json()

    def get_last_timestamp(self):
        response = requests.get(self.url + '/form/last%20timestamp.json')
        return response.json()

    def set_last_timestamp(self, timestamp):
        requests.patch(self.url + '/form/last%20timestamp.json', data=timestamp)

