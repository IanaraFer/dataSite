from backend.email_utils import send_payment_email

def handle_payment_submission(payment_info):
    subject = "Your Payment Confirmation"
    body = f"""
Thank you for your payment!

Details:
Amount: {payment_info.get('amount')}
Date: {payment_info.get('date')}
Reference: {payment_info.get('reference')}

If you have questions, reply to this email.

Regards,
DataSite Team
"""
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    username = "information@analyticacoreai.ie"
    password = "Maiaemolly22"
    recipient_email = payment_info.get('user_email')
    admin_email = "information@analyticacoreai.ie"

    send_payment_email(subject, body, recipient_email, admin_email, smtp_server, smtp_port, username, password)