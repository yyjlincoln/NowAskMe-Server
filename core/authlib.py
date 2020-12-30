from core.database import User, UserPrivate, EmailVerification, Token, UserStatus
import time
import logging
import secrets

def get_if_email_exists(email):
    return True if UserPrivate.objects(email__iexact=email).first() else False


def email_verification(email, otp):
    
    email = EmailVerification.objects(email__iexact=email).first()
    if not email:
        return -101

    email.attemptsLeft = email.attemptsLeft - 1
    if email.attemptsLeft <= 0:
        email.delete()
        return -104
    email.save()
    if time.time() - email.timestamp > 300:
        email.delete()
        return -102
    if email.otp.upper() != otp.upper():
        return -103
    email.delete()
    return 0


def get_uuid_by_email(email):
    obj = UserPrivate.objects(email__iexact=email).first()
    if obj:
        return obj.uuid
    return None


def get_user_info_by_uuid(uuid):
    return User.objects(uuid__iexact=uuid).first()

def get_user_private_by_uuid(uuid):
    return UserPrivate.objects(uuid__iexact=uuid).first()

def new_user(email):
    uuid = secrets.token_hex(16)
    try:
        newUserPublic = User(uuid=uuid)
        newUserPrivate = UserPrivate(uuid=uuid, registerationTime=time.time(), email=email)
        newUserPrivate.save()
        newUserPublic.save()
        return uuid
    except:
        return False

def new_token(uuid, scope):
    token = secrets.token_hex()
    user=get_user_info_by_uuid(uuid)
    token_entry = Token(token=token, scope=scope, expiry=time.time()+86400)
    user.tokens.append(token_entry)
    try:
        user.save()
        return token
    except Exception as e:
        logging.exception(e)
        return False

def get_user_status_by_uuid(uuid):
    if not get_user_info_by_uuid(uuid):
        return None

    user = UserStatus.objects(uuid__iexact=uuid).first()
    if not user:
        user = UserStatus(uuid=uuid)
        user.save()
    return user

def get_token_scope(uuid, token):
    user = get_user_status_by_uuid(uuid)
    if user:
        t = user.tokens.objects(token=token).first()
        if t:
            if t.expiry <= time.time():
                user.remove(t)
                return 'expired'

            return t.scope
        return None
    return None
