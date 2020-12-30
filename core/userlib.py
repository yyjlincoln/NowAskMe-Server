from core.database import User, UserPrivate
import core.authlib 

def update_user_profile(uuid, **properties):
    user = core.authlib.get_user_info_by_uuid(uuid)
    if not user:
        return -105

    if 'uuid' in properties:
        return False

    for prop in properties:
        if properties[prop]!=None:
            try:
                setattr(user, prop, properties[prop])
            except:
                return -113
        
    try:
        user.save()
        return 0
    except:
        return -114