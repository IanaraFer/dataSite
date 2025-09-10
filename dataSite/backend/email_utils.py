import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject, body, to_email, smtp_server, smtp_port, username, password):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=20) as server:
            server.set_debuglevel(1)  # Enable debug output
            server.starttls()
            server.login(username, password)
            server.sendmail(username, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")

# New function to send payment confirmation to both user and admin
def send_payment_email(subject, body, recipient_email, admin_email, smtp_server, smtp_port, username, password):
    # Send to user
    send_email(subject, body, recipient_email, smtp_server, smtp_port, username, password)
    # Send to admin
    send_email(subject, body, admin_email, smtp_server, smtp_port, username, password)