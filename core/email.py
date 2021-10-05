from core.emaillib.core import sendEmail
from core.emaillib.templates.general import NowaskmeGeneralEmail, NowaskmeLoginVerification
import secrets

def send_login_verification(email, name):
    otp = secrets.token_hex(3).upper()
    sendEmail(NowaskmeLoginVerification, subject="Your account verification code" ,email=email, name=name, code=otp, fromName = 'Nowaskme Account Verification')
    return otp