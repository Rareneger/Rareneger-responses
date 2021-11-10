from send import *
from message import *
from tqdm import tqdm

def confirm():
    print('')
    answer = input('Confirma? [S/N]: ')
    answer = answer.upper()
    if answer == 'S':
        return True
    elif answer == 'N':
        return False
    else:
        print('responda com S para sim ou N para não')
        return confirm()

if __name__ == '__main__':
    messager = Messager()
    msg = messager.make_message()
    messages = []
    while msg:
        messages.append(msg)
        
        if not confirm():
            messager.back_row()

        print('')
        msg = messager.make_message()

    messager.on_exit()

    if messages:
        whatsapp_sender =WhatsappSender()
        whatsapp_sender.do_login()
        email_sender = EmailSender()

        with tqdm(total=len(messages) * 10) as progress:
            for msg in messages:
                full_message, contact_email, contact_number = msg
                text_message, pay_message = full_message

                if not contact_number and not contact_email:
                    progress.update(10)
                rate = 2
                if not contact_number or not contact_email:
                    rate = 1

                if contact_number:
                    whatsapp_sender.send_message(text_message, contact_number, progress, rate * 2)
                    whatsapp_sender.send_message(pay_message, contact_number, progress, rate * 2)
                
                if contact_email:
                    email_sender.send_email(text_message + pay_message, contact_email)
                    progress.update(10 / rate)
