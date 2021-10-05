import datetime
from utils.AutoArguments import Arg
import core.authlib
import core.userlib

import utils.AutoArgValidators
from utils.ResponseModule import Res
from utils.AutoAuthentication import permission_control
import core.email


def attach(rmap):
    @rmap.register_request('/user/update_profile')
    @permission_control(scopes=['update_profile'])
    @Arg()
    def update_profile(uuid, name=None, userid=None, description=None):
        r = core.userlib.update_user_profile(uuid, name=name, userid=userid, description=description)
        if r==0:
            core.email.send_profile_update_alert(uuid)
        return Res(r)


    @rmap.register_request('/user/get_profile')
    @permission_control(scopes=['basic_view'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance)
    def get_profile(uuid, target=None):
        if not target:
            target = uuid

        u = core.userlib.get_user_info_by_uuid(target)
        return Res(0, uuid=u.uuid, userid=u.userid, name=u.name, description=u.description)

    @rmap.register_request('/user/get_following')
    @permission_control(scopes=['relation_view'])
    @Arg(start=int, limit=int, target=utils.AutoArgValidators.validate_user_existance)
    def get_following(uuid, target=None, start=0, limit=100):
        if not target:
            target = uuid
        return Res(0, following=core.userlib.get_following_by_uuid(uuid=target)[start:limit])

    @rmap.register_request('/user/get_pinned')
    @permission_control(scopes=['relation_view'])
    @Arg(start=int, limit=int)
    def get_pinned(uuid, start=0, limit=100):
        return Res(0, pinned=core.userlib.get_pinned_by_uuid(uuid=uuid)[start:limit])

    @rmap.register_request('/user/get_followers')
    @permission_control(scopes=['relation_view'])
    @Arg(start=int, limit=int, target=utils.AutoArgValidators.validate_user_existance)
    def get_followers(uuid, target=None, start=0, limit=100):
        if not target:
            target = uuid
        return Res(0, followers=core.userlib.get_followers_by_uuid(uuid))

    @rmap.register_request('/user/is_following')
    @permission_control(scopes=['relation_view'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance)
    def is_following(uuid, target):
        return Res(0, following=core.userlib.is_following(uuid, target))

    @rmap.register_request('/user/is_follower')
    @permission_control(scopes=['relation_view'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance)
    def is_follower(uuid, target):
        return Res(0, follower=core.userlib.is_following(target, uuid))
        # If target is following uuid, then to uuid, target is a follower.

    @rmap.register_request('/user/is_pinned')
    @permission_control(scopes=['relation_view'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance)
    def is_pinned(uuid, target):
        return Res(0, pinned=core.userlib.is_pinned(uuid, target))

    @rmap.register_request('/user/follow')
    @permission_control(scopes=['relation_write'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance)
    def follow(uuid, target):
        return Res(core.userlib.follow(uuid, target))

    @rmap.register_request('/user/unfollow')
    @permission_control(scopes=['relation_write'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance)
    def unfollow(uuid, target):
        return Res(core.userlib.unfollow(uuid, target))

    @rmap.register_request('/user/pin')
    @permission_control(scopes=['relation_write'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance)
    def pin(uuid, target):
        return Res(core.userlib.pin(uuid, target))

    @rmap.register_request('/user/unpin')
    @permission_control(scopes=['relation_write'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance)
    def unpin(uuid, target):
        return Res(core.userlib.unpin(uuid, target))

    @rmap.register_request('/user/search')
    @permission_control(scopes=['basic_view'])
    @Arg(start=int, limit=int)
    def search(term, start=0, limit=100):
        only_uuid = False
        only_userid = False
        only_name = False
        if term:
            if term[0] == '#':
                term = term[1:]
                only_userid = True
            elif term[0] == '!':
                term = term[1:]
                only_name = True
            elif term[0] == '$':
                term = term[1:]
                only_uuid = True

        ret = []
        for user in core.userlib.search(term, only_name=only_name, only_userid=only_userid, only_uuid=only_uuid):
            ret.append(user.uuid)
        return Res(0, results=ret[start:limit])

    @rmap.register_request('/user/set_beta')
    @permission_control(scopes=['update_profile'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance, status=lambda x: False if x.lower() == 'false' else True)
    def set_beta(uuid, status):
        if status:
            core.email.send_beta_join_alert(uuid)
        return Res(core.userlib.set_beta_status(uuid, status))

    @rmap.register_request('/user/get_beta')
    @permission_control(scopes=['basic_view'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance)
    def get_beta(uuid):
        return Res(0, status=core.userlib.get_beta_status(uuid))
