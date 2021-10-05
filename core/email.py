from core.emaillib.core import sendEmail
from core.emaillib.templates.general import NowaskmeGeneralEmail, NowaskmeLoginVerification
import secrets

def send_login_verification(email, name):
    otp = secrets.token_hex(3).upper()
    sendEmail(NowaskmeLoginVerification, email=email, name=name, code=otp, fromName = 'Nowaskme Accounts Verification')
    return otp