# import zmail
from credentials import Credentials
import random
import datetime
import time
import string
import secrets
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from core.database import EmailVerification
import os
import logging

def send_email(email, subject, message):
    try:
        if Credentials['debug']:
            # Don't actually send the email
            print(message)
            return True
    except KeyError:
        pass
    
    message = Mail(
        from_email='lincoln@nowask.me',
        to_emails=email,
        subject=subject,
        html_content=message)
    try:
        sg = SendGridAPIClient(Credentials['email']['apikey'])
        response = sg.send(message)
        return True
    except Exception as e:
        return False


def send_login_verification(email, name=None):
    existingVerification = EmailVerification.objects(email__iexact=email).first()
    if existingVerification:
        existingVerification.delete()
        print('Deleted old verif')
    

    otp = secrets.token_hex(3).upper()

    result = send_email(email, 'NAM Email Verification',
    f'''
    <p>Hey <b>{email if name==None else name}</b>,</p>
    <p>You've just requested to authenticate yourself at {datetime.datetime.fromtimestamp(time.time()).isoformat()}.</p>
    <hr></hr>
    <p>If that was you, please enter the following OTP to continue:</p>
    <p style="font-size: 2em; text-align: center;"><b>{otp}</b></p>
    <hr></hr>
    <p>Otherwise, please ignore this email.</p>
    <p>Best regards,</p>
    <p>Lincoln from NowAsk.me</p>''')
    print(result)
    if result:
        try:
            newVerification = EmailVerification(email = email, otp = otp, timestamp=time.time(), scope='login')
            newVerification.save()
        except Exception as e:
            print(e)
            logging.warn('Could not save the verification code to database!')
            return False
        return True
    return False
