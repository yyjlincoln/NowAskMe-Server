import datetime
from utils.AutoArguments import Arg
import core.authlib
import core.emaillib
import core.userlib

import utils.AutoArgValidators
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
        u = core.userlib.get_user_info_by_uuid(uuid)
        if u:
            return Res(0, uuid=u.uuid, userid=u.userid, name=u.name, description=u.description)
        return Res(-105)

    @rmap.register_request('/user/get_following')
    @permission_control(scopes=['relation_view'])
    @Arg(start=int, limit=int, target=utils.AutoArgValidators.validate_user_existance)
    def get_following(uuid, target=None, start=0, limit=100):
        if not target:
            target = uuid
        u = core.userlib.get_user_relations_by_uuid(uuid=target)
        if u:
            return Res(0, following=u.following[start:limit])
        return Res(0, following=[])

    @rmap.register_request('/user/get_followers')
    @permission_control(scopes=['relation_view'])
    @Arg(start=int, limit=int, target=utils.AutoArgValidators.validate_user_existance)
    def get_followers(uuid, target=None, start=0, limit=100):
        if not target:
            target = uuid
        users = core.userlib.get_user_followers_relation_by_uuid(uuid=target)
        if users:
            # Generate a list of followers
            ret = []
            for user in users:
                ret.append(user.uuid)
            return Res(0, followers=ret[start:limit])
        return Res(0, followers=[])
