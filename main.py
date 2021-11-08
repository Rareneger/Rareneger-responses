from send import *
from message import *

if __name__ == '__main__':
    messager = Messager()
    whatsapp =WhatsappSender()
    whatsapp.do_login()
    msg = messager.make_message()
    while msg:
        if msg:
            message, email, number = msg
            if number:
                whatsapp.send_message(message, number)
            
            msg = messager.make_message()
    messager.on_exit()
