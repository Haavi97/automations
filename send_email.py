import smtplib
from dotenv import load_dotenv, find_dotenv
from os import getenv


# init
load_dotenv(find_dotenv())
sender = getenv('SENDER')
receiver = getenv('RECEIVER')
pswd = getenv('PSWD')


def send_email(subject, body, email_to=receiver, add=''):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender, pswd)
    if add == '':
        msg = 'Subject:{}\n\n{}'.format(subject, body)
    else:
        try:
            msg = ('From:{}\r\n' +
                   'To:{}\r\n' +
                   '{}'
                   'Subject:{}\r\n{}').format(sender, ','.join(email_to), add, subject, body)
        except:
            print('Wrong additional part format.')
            return -1
    msg = msg.encode('utf-8', 'ignore')

    print('Sending from:\t{} \nto:\t\t{}\n\n'.format(sender, email_to))

    server.sendmail(sender, email_to, msg)

    print('Message sent:\n\n' + str(msg.decode('utf-8'))+'\n\n')

    server.quit()
