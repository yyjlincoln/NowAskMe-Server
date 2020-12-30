from core.database import User, UserPrivate, EmailVerification
import time


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
    if email.otp.lower() != otp.lower():
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


def new_token(uuid, scope):
    # [TODO]
    token = '12345'
    return token
