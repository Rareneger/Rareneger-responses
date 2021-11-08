import pandas as pd

try:
    with open('personal-infos/url_form.txt', 'r') as file:
        url = file.read()
except FileNotFoundError:
    print('the url file was not find')

try:
    with open('personal-infos/last_timestamp.txt', 'r') as file:
        last_timestamp = file.read()
except FileNotFoundError:
    print('the timestamp file was not find')

try:
    form_df = pd.read_csv(url)
except OSError:
    print('something failure opening your url')

initial_row = 0
if last_timestamp:
    for i, timestamp in enumerate(form_df['Timestamp ']):
        if timestamp == last_timestamp:
            initial_row = i + 1
            break

last_timestamp = form_df['Timestamp '][len(form_df) - 1]
try:
    with open('personal-infos/last_timestamp.txt', 'w') as file:
        file.write(last_timestamp)
except FileNotFoundError:
    print('the timestamp file was not find')

for row in range(initial_row, len(form_df)):
    name = form_df['Nome: '][row]
    contact_way = form_df['Por onde deseja receber as informações de confirmação do atendimento? '][row]
    
    if 'Whatsapp' in contact_way:
        contact_number = form_df['Para receber por Whatsapp informe o número de celular: '][row]
    if 'Email' in contact_way:
        contact_email = form_df['Para receber por Email informe o Email: '][row]

    attendance_kind = form_df['Atendimento '][row].split('-')[0].strip()
    schedule_possibilities = f'{form_df["Início "][row]} e {form_df["Fim "][row]}'

    print(f'Marque uma {attendance_kind}, a pessoa está disponível entre {schedule_possibilities} nos dias {form_df["Disponibilidade de dias da semana "][row]}')

    mark_date = input('digite a data: ')

    mark_schedule = input('digite o hórario: ')

    print('A menssagem a ser enviada será: ')
    menssagem = f'Olá {name}, tudo bem? aqui é o Rareneger \nA sua {attendance_kind} está marcada para {mark_date} as {mark_schedule}.' 
    print('')
    print(menssagem)

