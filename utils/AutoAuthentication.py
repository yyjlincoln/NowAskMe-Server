from utils.AutoArguments import Arg
from functools import wraps
import core.authlib
from utils.ResponseModule import Res
from commons import NAMExceptions

# ScopeGroup -- MicroScope

scopeList = {
    'login': [
        'update_profile',
        'basic_view',
        'basic_write',
        'renew_token',
        'post_view',
        'post_write',
        'relation_view',
        'relation_write'
    ],
    'expired':{},
}


def permission_control(scopes=['basic_view','baisc_write']):
    # for scope in scopes:
    #     if scope not in scopeList:
    #         raise NAMExceptions(f'Invalid scope \'{scope}\'!')
    def _permission_control(func):
        @wraps(func)
        @Arg()
        def __permission_control(uuid=None, token=None, *args, **kw):
            if scopes != []:
                if not uuid or not token:
                    return Res(-107) 

                scope = core.authlib.get_token_scope(uuid, token)
                if not scope:
                    return Res(-108)
                
                if scope=='expired':
                    return Res(-109)                
                
                if scope not in scopeList:
                    return Res(-110, scope = scope)
                
                for sc in scopes: # For all required scopes
                    if sc not in scopeList[scope]: # If the current scope group does not satisfy all scopes
                        return Res(-111, scope = sc)
                
                # All good now

                return func(*args, **kw)
        return __permission_control
    return _permission_control


def authenticate(scope):
    pass
