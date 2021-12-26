import core.authlib
import core.userlib
import utils.ConvertAndValidate
import core.email
from GlobalContext import API


@API.endpoint('update-profile', {
    'scopes': ['update_profile'],
    'httproute': '/user/update_profile'
})
def update_profile(uuid, makeResponse, name=None, userid=None, description=None):
    r = core.userlib.update_user_profile(
        uuid, name=name, userid=userid, description=description)
    if r == 0:
        core.email.send_profile_update_alert(uuid)
    return makeResponse(r)


@API.endpoint('get-profile', {
    'scopes': ['basic_view'],
    'httproute': '/user/get_profile'
}, target=utils.ConvertAndValidate.validate_user_existance)
def get_profile(uuid, makeResponse, target=None):
    if not target:
        target = uuid
    u = core.userlib.get_user_info_by_uuid(target)
    return makeResponse(0, uuid=u.uuid, userid=u.userid, name=u.name, description=u.description)


@API.endpoint('get-following', {
    'scopes': ['relation_view'],
    'httproute': '/user/get_following'
}, start=int, limit=int, target=utils.ConvertAndValidate.validate_user_existance)
def get_following(uuid, makeResponse, target=None, start=0, limit=100):
    if not target:
        target = uuid
    return makeResponse(0, following=core.userlib.get_following_by_uuid(uuid=target)[start:limit])


@API.endpoint('get-pinned', {
    'scopes': ['relation_view'],
    'httproute': '/user/get_pinned'
}, start=int, limit=int)
def get_pinned(uuid, makeResponse, start=0, limit=100):
    return makeResponse(0, pinned=core.userlib.get_pinned_by_uuid(uuid=uuid)[start:limit])


@API.endpoint('get-followers', {
    'scopes': ['relation_view'],
    'httproute': '/user/get_followers'
}, start=int, limit=int, target=utils.ConvertAndValidate.validate_user_existance)
def get_followers(uuid, makeResponse, target=None, start=0, limit=100):
    if not target:
        target = uuid
    return makeResponse(0, followers=core.userlib.get_followers_by_uuid(uuid))


@API.endpoint('is-following', {
    'scopes': ['relation_view'],
    'httproute': '/user/is_following'
}, target=utils.ConvertAndValidate.validate_user_existance)
def is_following(uuid, target, makeResponse):
    return makeResponse(0, following=core.userlib.is_following(uuid, target))


@API.endpoint('is-follower', {
    'scopes': ['relation_view'],
    'httproute': '/user/is_follower'
}, target=utils.ConvertAndValidate.validate_user_existance)
def is_follower(uuid, target, makeResponse):
    return makeResponse(0, follower=core.userlib.is_following(target, uuid))
    # If target is following uuid, then to uuid, target is a follower.


@API.endpoint('is-pinned', {
    'scopes': ['relation_view'],
    'httproute': '/user/is_pinned'
}, target=utils.ConvertAndValidate.validate_user_existance)
def is_pinned(uuid, target, makeResponse):
    return makeResponse(0, pinned=core.userlib.is_pinned(uuid, target))


@API.endpoint('follow', {
    'scopes': ['relation_write'],
    'httproute': '/user/follow'
}, target=utils.ConvertAndValidate.validate_user_existance)
def follow(uuid, target, makeResponse):
    return makeResponse(core.userlib.follow(uuid, target))


@API.endpoint('unfollow', {
    'scopes': ['relation_write'],
    'httproute': '/user/unfollow'
}, target=utils.ConvertAndValidate.validate_user_existance)
def unfollow(uuid, target, makeResponse):
    return makeResponse(core.userlib.unfollow(uuid, target))


@API.endpoint('pin', {
    'scopes': ['relation_write'],
    'httproute': '/user/pin'
}, target=utils.ConvertAndValidate.validate_user_existance)
def pin(uuid, target, makeResponse):
    return makeResponse(core.userlib.pin(uuid, target))


@API.endpoint('unpin', {
    'scopes': ['relation_write'],
    'httproute': '/user/unpin'
}, target=utils.ConvertAndValidate.validate_user_existance)
def unpin(uuid, target, makeResponse):
    return makeResponse(core.userlib.unpin(uuid, target))


@API.endpoint('search', {
    'scopes': ['basic_view'],
    'httproute': '/user/search'
}, start=int, limit=int)
def search(term, makeResponse, start=0, limit=100):
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
    return makeResponse(0, results=ret[start:limit])


@API.endpoint('set-beta', {
    'scopes': ['update_profile'],
    'httproute': '/user/set_beta'
}, status=lambda x: False if x.lower() == 'false' else True)
def set_beta(uuid, status, makeResponse):
    r = core.userlib.set_beta_status(uuid, status)
    if status and r == 0:
        core.email.send_beta_join_alert(uuid)
    return makeResponse(r)


@API.endpoint('get-beta', {
    'scopes': ['basic_view'],
    'httproute': '/user/get_beta'
})
def get_beta(uuid, makeResponse):
    return makeResponse(0, status=core.userlib.get_beta_status(uuid))
