import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_payment_email(subject, body, recipient_email, admin_email, smtp_server, smtp_port, username, password):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Send to recipient
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(username, recipient_email, msg.as_string())

    # Send copy to admin
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(username, admin_email, msg.as_string())