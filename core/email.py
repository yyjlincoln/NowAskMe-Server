from os import name
from core.emaillib.core import sendEmail
from core.emaillib.templates.general import NowaskmeGeneralEmail, NowaskmeLoginVerification
from core.database import EmailVerification
import core.userlib
import time
import logging
import secrets
import json


def send_login_verification(email, name):
    otp = secrets.token_hex(3).upper()
    result = sendEmail(NowaskmeLoginVerification, subject="Your account verification code" ,email=email, name=name, code=otp, fromName = 'Nowaskme Account Verification')
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

def send_welcome_email(uuid):
    user = core.userlib.get_user_info_by_uuid(uuid)
    userPrivate = core.userlib.get_user_info_by_uuid(uuid)
    if not user or not userPrivate:
        return False

    email = userPrivate.email
    result = sendEmail(NowaskmeGeneralEmail, subject="Welcome to Nowaskme!", email=email, title = "Thanks for signing up!", content = f'''Welcome on board!

Your account has been created. Please keep this email for your records.

Email: {email}
Unique UUID: {uuid}

Nowask.me is an anomynous Q&amp;A platform. It's a place where you can ask questions and get answers from other people, anomynously.

The platform had not been fully built - and it probably will not be. It's a HSC major work project - and it's good enough for now. You'll find that a lot of the functionalities have not been implemented just yet.

For more information, please visit https://yyjlincoln.com/portfolio/nowaskme/ - where you can find its source code, project planning &amp; testing document and so on.

You can also check out my other projects or know more about me at https://yyjlincoln.com/.

Thanks for your continued support.''')
    if result:
        return True
    return False

def send_profile_update_alert(uuid):
    user = core.userlib.get_user_info_by_uuid(uuid)
    userPrivate = core.userlib.get_user_info_by_uuid(uuid)
    if not user or not userPrivate:
        return False

    email = userPrivate.email
    result = sendEmail(NowaskmeGeneralEmail, subject="You've updated your user profile", email=email, name = user.name, title = "You've updated your user profile.", content = f'''Here's how your new profile looks like:

Name: {user.name}
UserID: {user.userid}
Description: {user.description}
Unique UUID: {uuid}''')
    if result:
        return True
    return False

def send_beta_join_alert(uuid):
    user = core.userlib.get_user_info_by_uuid(uuid)
    userPrivate = core.userlib.get_user_info_by_uuid(uuid)
    if not user or not userPrivate:
        return False

    email = userPrivate.email
    result = sendEmail(NowaskmeGeneralEmail, subject="You've joined nowaskme beta.", email=email, name = user.name, title = "Thanks for joining our beta testing.", content = f'''Thanks for joining our beta testing! You now have the access to our beta features. Here's a list of features that you can enjoy:
    
{json.dumps(core.configlib.get_config_by_uuid(uuid), indent=4, sort_keys=True)}
''')
    if result:
        return True
    return False