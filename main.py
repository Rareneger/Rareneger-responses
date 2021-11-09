from send import *
from message import *

def confirm():
    answer = input('Confirma? [S/N]: ')
    answer = answer.upper()
    if answer == 'S':
        return True
    elif answer == 'N':
        return False
    else:
        print('responda com S para sim ou N para não')
        print('')
        return confirm()

if __name__ == '__main__':
    messager = Messager()
    msg = messager.make_message()
    messages = []
    while msg:
        messages.append(msg)
        text, email, number = msg
        
        if not number and not email:
            print('* A pessoa não disponibilizou meios de contato')
        
        if not confirm():
            messager.back_row()

        print('')
        msg = messager.make_message()

    messager.on_exit()

    if messages:
        whatsapp =WhatsappSender()
        whatsapp.do_login()

        for msg in messages:
            text, email, number = msg
            if number:
                whatsapp.send_message(text, number)
