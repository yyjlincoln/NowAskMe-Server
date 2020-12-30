from utils.AutoArguments import Arg
from functools import wraps

scopeList = {
    'login': [
        'edit_profiles',
        'basic_view',
        'basic_write',
        'renew_token',
        'post',
    ]
}


def permission_control(scopes=['basic_view','baisc_write']):
    def _permission_control(func):
        @Arg()
        @wraps(func)
        def __permission_control(*args, **kw):
            pass


def authenticate(scope):
    pass
