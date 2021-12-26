import core.userlib
import core.postlib
from .RequestMap.Exceptions import ValidationError


def validate_user_existance(uuid):
    'The provided uuid must be associated with an existing user. If it is, return the uuid; otherwise, raise an exception.'
    if uuid:
        if core.userlib.get_user_info_by_uuid(uuid):
            return uuid
        raise ValidationError(-105)


def validate_post_existance(postid):
    post = core.postlib.get_post_by_postid(postid)
    if not post:
        raise ValidationError(-118)
    return postid
