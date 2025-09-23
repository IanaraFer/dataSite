import os
import json
import sendgrid
from sendgrid.helpers.mail import Mail

def handler(event, context):
    try:
        body = json.loads(event['body'])
        email = body.get('email')
        if not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Email is required.'})
            }
        # SendGrid setup
        SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
        TO_EMAIL = os.environ.get('PROMO_TO_EMAIL')  # Set this in Netlify env vars
        if not SENDGRID_API_KEY or not TO_EMAIL:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Server configuration error.'})
            }
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        message = Mail(
            from_email=TO_EMAIL,
            to_emails=TO_EMAIL,
            subject='New Newsletter Signup',
            html_content=f'<p>New subscriber: {email}</p>'
        )
        response = sg.send(message)
        if response.status_code in [200, 202]:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Subscription successful.'})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to send email.'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
