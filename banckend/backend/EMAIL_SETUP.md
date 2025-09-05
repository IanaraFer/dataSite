# Outlook SMTP Email Notification Setup

This integration sends payment confirmation emails to both the paying user and the admin/owner.

## Payment Notification Emails

When a user completes a payment, the system sends:
- A confirmation email to the user.
- An automatic copy to the admin/owner for records.

## Configuration

Set your admin email and SMTP credentials in your environment or in the code.
```
OUTLOOK_EMAIL=analyticacoreai@outlook.com
OUTLOOK_PASSWORD=Maiaemolly22
ADMIN_EMAIL=analyticacoreai@outlook.com
```
**Never commit your `.env` file or hardcode credentials in production.**

## Customization

You can modify the payment notification text in `trial_server.py`.

## Troubleshooting

- Ensure your Outlook account allows SMTP access.
- If using 2FA, create an App Password.
- Check your spam folder if emails aren’t received.
- Log errors for failed sends.