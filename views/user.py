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
        u = core.userlib.get_user_relations_by_uuid(uuid=target)
        if u:
            return Res(0, following=u.following[start:limit])
        return Res(0, following=[])

    @rmap.register_request('/user/get_pinned')
    @permission_control(scopes=['relation_view'])
    @Arg(start=int, limit=int)
    def get_pinned(uuid, start=0, limit=100):
        # Pinned is private
        u = core.userlib.get_user_relations_by_uuid(uuid=uuid)
        if u:
            return Res(0, pinned=u.pinned[start:limit])
        return Res(0, pinned=[])

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


    @rmap.register_request('/user/is_following')
    @permission_control(scopes=['relation_view'])
    @Arg(start=int, limit=int, target=utils.AutoArgValidators.validate_user_existance)
    def is_following(uuid, target, start=0, limit=100):
        u = core.userlib.get_user_relations_by_uuid(uuid=uuid)
        if u:
            if target.lower() in [x.lower() for x in u.following]:
                return Res(0, following=True)
        return Res(0, following=False)

    @rmap.register_request('/user/is_follower')
    @permission_control(scopes=['relation_view'])
    @Arg(start=int, limit=int, target=utils.AutoArgValidators.validate_user_existance)
    def is_follower(uuid, target, start=0, limit=100):
        u = core.userlib.get_user_relations_by_uuid(uuid=target)
        if u:
            if uuid.lower() in [x.lower() for x in u.following]:
                return Res(0, follower=True)
        return Res(0, follower=False)

    # @rmap.register_request('/user/follow')
    # @permission_control(scopes=['relation_view'])
    # @Arg(start=int, limit=int, target=utils.AutoArgValidators.validate_user_existance)
    # def is_follower(uuid, target, start=0, limit=100):
    #     u = core.userlib.get_user_relations_by_uuid(uuid=target)
    #     if u:
    #         if uuid.lower() in [x.lower() for x in u.following]:
    #             return Res(0, follower=True)
    #     return Res(0, follower=False)
