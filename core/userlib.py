from core.database import User, UserPrivate, UserRelations, UserStatus
import core.authlib


def update_user_profile(uuid, **properties):
    user = get_user_info_by_uuid(uuid)
    if not user:
        return -105

    if 'uuid' in properties:
        return False

    for prop in properties:
        if properties[prop] != None:
            try:
                setattr(user, prop, properties[prop])
            except:
                return -113

    try:
        user.save()
        return 0
    except:
        return -114


def get_user_status_by_uuid(uuid):
    if not core.userlib.get_user_info_by_uuid(uuid):
        return None

    user = UserStatus.objects(uuid__iexact=uuid).first()
    if not user:
        user = UserStatus(uuid=uuid)
        user.save()
    return user


def get_user_followers_relation_by_uuid(uuid):
    'Returns [UserRelations(), ...] of users who has <uuid> in their following.'
    return UserRelations.objects(following__iexact=uuid)

def get_user_relations_by_uuid(uuid):
    return UserRelations.objects(uuid__iexact=uuid).first()


def get_user_info_by_uuid(uuid):
    return User.objects(uuid__iexact=uuid).first()


def get_user_private_by_uuid(uuid):
    return UserPrivate.objects(uuid__iexact=uuid).first()
