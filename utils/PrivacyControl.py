import core.privacylib
from functools import wraps
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
    priv = core.privacylib.get_user_privacy_options(postedBy)
