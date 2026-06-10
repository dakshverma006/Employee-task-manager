import sendgrid
from sendgrid.helpers.mail import Mail
from flask import current_app

def send_email(to_email, subject, body):
    try:
        sg = sendgrid.SendGridAPIClient(
            api_key=current_app.config['SENDGRID_API_KEY']
        )
        message = Mail(
            from_email=current_app.config['MAIL_FROM'],
            to_emails=to_email,
            subject=subject,
            html_content=body
        )
        sg.send(message)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False