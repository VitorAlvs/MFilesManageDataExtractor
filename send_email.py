import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import config

load_dotenv(encoding='utf-8')

def send_alert_email():
    message = Mail(
        from_email=config.SENDGRID_FROM_EMAIL,
        to_emails=config.SENDGRID_EMAIL_RECIPIENTS, # List of (email, name) tuples
        subject='Alert | M-Files Manage Data Extractor',
        html_content='The header structure of the CSVs extracted from M-Files Manage has changed. Please check the new structure and update the code.')
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e: # Catching generic Exception for robustness
        print(f"Error sending email: {e}")
