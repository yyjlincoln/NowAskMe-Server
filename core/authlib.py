from core.database import User, UserPrivate


def get_if_email_exists(email):
    return True if UserPrivate.objects(email__iexact=email).first() else False
