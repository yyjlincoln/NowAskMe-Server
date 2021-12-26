from core.database import User, UserPrivate, UserRelations, UserStatus
import core.authlib
from mongoengine.queryset.visitor import Q


def update_user_profile(uuid, **properties):
    user = get_user_info_by_uuid(uuid)
    if not user:
        return -105

    if 'uuid' in properties:
        return False

    for prop in properties:
        if properties[prop] is not None:
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


def set_beta_status(uuid, status):
    user = get_user_info_by_uuid(uuid)
    if not user:
        return -105
    user.beta = status
    user.save()
    return 0


def get_beta_status(uuid):
    user = get_user_info_by_uuid(uuid)
    if not user:
        return False
    return user.beta


def get_user_relations_by_uuid(uuid):
    return UserRelations.objects(uuid__iexact=uuid).first()


def get_user_info_by_uuid(uuid):
    return User.objects(uuid__iexact=uuid).first()


def get_user_private_by_uuid(uuid):
    return UserPrivate.objects(uuid__iexact=uuid).first()


def get_following_by_uuid(uuid):
    u = get_user_relations_by_uuid(uuid=uuid)
    if u:
        return u.following
    return []


def get_pinned_by_uuid(uuid):
    u = get_user_relations_by_uuid(uuid=uuid)
    if u:
        return u.pinned
    return []


def get_followers_by_uuid(uuid):
    users = get_user_followers_relation_by_uuid(uuid=uuid)
    ret = []
    if users:
        # Generate a list of followers
        for user in users:
            ret.append(user.uuid)
    return ret


def is_following(uuid, target):
    u = get_user_relations_by_uuid(uuid=uuid)
    if u:
        if target.lower() in [x.lower() for x in u.following]:
            return True
    return False


def is_pinned(uuid, target):
    u = get_user_relations_by_uuid(uuid=uuid)
    if u:
        if target.lower() in [x.lower() for x in u.pinned]:
            return True
    return False


def follow(uuid, target):
    if is_following(uuid, target):
        return 101
    u = get_user_relations_by_uuid(uuid)
    if not u:
        u = UserRelations(uuid=uuid)
        u.save()
    try:
        u.following.append(target)
        u.save()
        return 0
    except:
        return -114


def unfollow(uuid, target):
    if not is_following(uuid, target):
        return 102
    u = get_user_relations_by_uuid(uuid)
    if not u:
        u = UserRelations(uuid=uuid)
        u.save()
    try:
        u.following.remove(target)
        u.save()
        return 0
    except:
        return -114


def pin(uuid, target):
    if is_pinned(uuid, target):
        return 103
    u = get_user_relations_by_uuid(uuid)
    if not u:
        u = UserRelations(uuid=uuid)
        u.save()
    try:
        u.pinned.append(target)
        u.save()
        return 0
    except:
        return -114


def unpin(uuid, target):
    if not is_pinned(uuid, target):
        return 104
    u = get_user_relations_by_uuid(uuid)
    if not u:
        u = UserRelations(uuid=uuid)
        u.save()
    try:
        u.pinned.remove(target)
        u.save()
        return 0
    except:
        return -114


def search(term, only_uuid=False, only_userid=False, only_name=False):
    if only_uuid:
        query = User.objects(Q(uuid__iexact=term))
    elif only_userid:
        query = User.objects(Q(userid__icontains=term))
    elif only_name:
        query = User.objects(Q(name__icontains=term))
    else:
        query = User.objects(Q(uuid__iexact=term) | Q(
            userid__icontains=term) | Q(name__icontains=term))
    return query
