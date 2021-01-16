import core.privacylib
from functools import wraps
import core.postlib
import core.userlib

# ======TODO======


def privacy(privacy_type='post'):
    def _privacy(func):
        @wraps(func)
        def __privacy(*args, **kw):
            privacy_check(privacy_type, *args, **kw)
            return func(*args, **kw)
        return __privacy
    return _privacy


def privacy_check(privacy_type):
    pass

# ======TODO END======


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

    # if priv == 'private':
    #     if str(post.uuid).lower() == str(accessFrom).lower():
    #         return True
    # Included in the first case

    return False


def get_post_privacy_options(postid):
    post = core.postlib.get_post_by_postid(postid)
    if post.privacy == 'inherit' or not post.privacy:
        try:
            return core.privacylib.get_user_privacy_options(uuid=post.uuid).post
        except:
            return 'private'
    return post.privacy
