from core.database import UserPrivacy, Post

def get_user_privacy_options(uuid):
    return UserPrivacy.objects(uuid__iexact=uuid).first()
    
