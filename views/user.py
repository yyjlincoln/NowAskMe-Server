import datetime
from utils.AutoArguments import Arg
import core.authlib
import core.emaillib
import core.userlib

from utils.ResponseModule import Res
from utils.AutoAuthentication import permission_control


def attach(rmap):
    @rmap.register_request('/user/update_profile')
    @permission_control(scopes=['update_profile'])
    @Arg()
    def update_profile(uuid, name=None, userid=None, description=None):
        return Res(core.userlib.update_user_profile(uuid, name=name, userid=userid, description=description))

    @rmap.register_request('/user/get_profile')
    @permission_control(scopes=['basic_view'])
    @Arg()
    def get_profile(uuid):
        u = core.userlib.get_user_profile(uuid)
        if u:
            return Res(0, uuid=u.uuid, userid=u.userid, name=u.name, description=u.description)
        return Res(-105)
