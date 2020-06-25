import os
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(fromAddr, to, subject, text, files):
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = ', '.join(to)
    outer['From'] = fromAddr

    outer.attach(MIMEText(text))

    for filename in files:
        path = os.path.join('attachments', filename)
        if not os.path.isfile(path):
            continue

        fp = open(path, 'rb')
        msg = MIMEBase('application', 'octet-stream')
        msg.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(msg)

        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        outer.attach(msg)

    s = smtplib.SMTP('smtp.yandex.ru: 587')
    s.starttls()
    s.login(outer['From'], '1q1a2w2s')

    s.sendmail(fromAddr, to, outer.as_string())
    s.quit()


if __name__ == '__main__':
    fromAddr = 'server5mtp@yandex.com'

    conf = iter(open('config.txt', 'r', encoding='utf-8').read().splitlines())

    to = list()
    addr = next(conf)
    while addr != 'Subject:':
        addr = next(conf)
        to.append(addr)

    subject = next(conf)
    next(conf)

    with open('text.txt', encoding='utf-8') as file:
        text = file.read()
    files = list(conf)
    send_email(fromAddr, to, subject, text, files)
