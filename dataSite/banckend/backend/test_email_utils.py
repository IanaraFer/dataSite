import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
from email_utils import send_payment_email

def test_send_payment_email():
    subject = "Test Payment Confirmation"
    body = "This is a test email for payment confirmation."
    recipient_email = "your_test_email@example.com"  # Change to your email for testing
    admin_email = "analyticacoreai@outlook.com"
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    username = "analyticacoreai@outlook.com"
    password = "Maiaemolly22"

    print("Attempting to send payment confirmation email...")
    try:
        send_payment_email(
            subject,
            body,
            recipient_email,
            admin_email,
            smtp_server,
            smtp_port,
            username,
            password
        )
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Error sending test email: {e}")

if __name__ == "__main__":
    test_send_payment_email()