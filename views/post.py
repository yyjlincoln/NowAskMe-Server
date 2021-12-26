import utils.ConvertAndValidate
import core.postlib
import core.privacylib
from GlobalContext import API


@API.endpoint('get-post', {
    'scopes': ['post_view'],
    'httproute': '/post/get_post'
}, postid=utils.ConvertAndValidate.validate_post_existance)
def post_get_post(uuid, postid, makeResponse):
    'Gets post by postid.'
    # Postid has been validated and exists
    if not core.privacylib.post_privacy(postid, accessFrom=uuid):
        return makeResponse(-119)
    post = core.postlib.get_post_by_postid(postid)
    return makeResponse(0, post={
        'content': post.content,
        'time': post.time,
        'type': post.posttype,
        'postid': post.postid,
        'uuid': post.uuid,
        'privacy': post.privacy
    })


@API.endpoint('get-user-stream', {
    'scopes': ['post_view'],
    'httproute': '/post/get_user_stream'
}, target=utils.ConvertAndValidate.validate_user_existance)
def post_get_user_post(uuid, target, makeResponse):
    stream = core.postlib.get_user_stream(uuid, target)
    return makeResponse(0, stream=stream)


@API.endpoint('get-stream', {
    'scopes': ['post_view'],
    'httproute': '/post/get_stream'
})
def post_get_stream(uuid, makeResponse):
    stream = core.postlib.get_stream(uuid)
    return makeResponse(0, stream=stream)


@API.endpoint('new-post', {
    'scopes': ['post_write'],
    'httproute': '/post/new_post'
})
def new_post(uuid, content, type, makeResponse, privacy='inherit'):
    postid = core.postlib.new_post(
        uuid=uuid, content=content, posttype=type, privacy=privacy)
    if not postid:
        return makeResponse(-114)
    return makeResponse(0, postid=postid)


@API.endpoint('delete-post', {
    'scopes': ['post_write'],
    'httproute': '/post/delete_post'
}, postid=utils.ConvertAndValidate.validate_post_existance)
def delete_post(uuid, postid, makeResponse):
    post = core.postlib.get_post_by_postid(postid)
    if post.uuid.lower() == uuid:
        post.delete()
        return makeResponse(0)
    return makeResponse(-120)
