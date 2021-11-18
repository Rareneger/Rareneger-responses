import pandas as pd

class MockInfo():
    
    def get_email(self):
        return 'mock email'

    def get_email_password(self):
        return 'mock password'

    def get_pay_codes(self):
        mock_pay_codes = {
            'Consulta' : 'mock consulta pay code',
            'Leitura de Tarot' : 'mock leitura de tarot pay code',
            'Mentoria' : 'mock mentoria pay code',
            'Radiestesia' : 'mock radiestesia pay code'}
        return mock_pay_codes

    def get_last_timestamp(self):
        return 'mock last_timestamp'

    def set_last_timestamp(self, timestamp):
        pass

    def google_login(self):
        return 'mock creds'

    def get_form_df(self):
        values = [['Carimbo de data/hora', 'Nome:',
        'Para receber a confirmação por Email, informe o Email:',
        'Atendimento', 'Modalidade', 'Início', 'Fim',
        'Disponibilidade de dias da semana']]
        for j in range(5):
            values.append([f'({i},{j})' for i, value in enumerate(values[0])])
        return pd.DataFrame(values[1:], columns=values[0])

if __name__ == '__main__':
    pass