import os
import ssl
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def send_email(body, subject, sender_password,
               receiver_email='leonardomichalskim@gmail.com',
               sender_email='leonardomichalskim@gmail.com',
               file_attachment_list=[]):
    port = 465  # For SSL

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['to'] = receiver_email
    msg.attach(MIMEText(body, 'plain'))

    for filename in file_attachment_list:
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.split(filename)[-1]}'
        )
        msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', port,
                          context=ssl.create_default_context()) as server:
        server.login(msg['From'], sender_password)
        server.sendmail(msg['From'], msg['to'], msg.as_string())
