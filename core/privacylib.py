import core.postlib
from core.database import UserPrivacy


def get_user_privacy_options(uuid):
    return UserPrivacy.objects(uuid__iexact=uuid).first()


def post_privacy(postid, accessFrom):
    post = core.postlib.get_post_by_postid(postid)
    priv = get_post_privacy_options(postid)
    if str(post.uuid).lower() == str(accessFrom).lower():
        return True

    if priv == 'public':
        return True
    if priv == 'following':
        if core.userlib.is_following(post.uuid, accessFrom):
            return True
    if priv == 'followers':
        if core.userlib.is_following(accessFrom, post.uuid):
            return True
    return False


def get_post_privacy_options(postid):
    post = core.postlib.get_post_by_postid(postid)
    if post.privacy == 'inherit' or not post.privacy:
        try:
            return get_user_privacy_options(uuid=post.uuid).post
        except Exception:
            return 'private'
    return post.privacy
