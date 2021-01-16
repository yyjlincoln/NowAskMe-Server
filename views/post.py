from utils.AutoArguments import Arg
from utils.AutoAuthentication import permission_control
from utils.ResponseModule import Res
import utils.AutoArgValidators
import core.postlib
import utils.PrivacyControl
import time


def attach(rmap):
    @rmap.register_request('/post/get_post')
    @permission_control(['post_view'])
    @Arg(postid=utils.AutoArgValidators.validate_post_existance)
    def post_get_post(uuid, postid):
        'Gets post by postid.'
        # Postid has been validated and exists
        if not utils.PrivacyControl.post_privacy(postid, accessFrom=uuid):
            return Res(-119)
        post = core.postlib.get_post_by_postid(postid)
        return Res(0, post={
            'content': post.content,
            'time': post.time,
            'type': post.posttype,
            'postid': post.postid,
            'uuid': post.uuid,
            'privacy': post.privacy
        })

    @rmap.register_request('/post/get_user_stream')
    @permission_control(['post_view'])
    @Arg(target=utils.AutoArgValidators.validate_user_existance)
    def post_get_user_post(uuid, target):
        stream = core.postlib.get_user_stream(uuid, target)
        return Res(0, stream=stream)

    @rmap.register_request('/post/get_stream')
    @permission_control(['post_view'])
    @Arg()
    def post_get_stream(uuid):
        # TODO: Add limit
        stream = core.postlib.get_stream(uuid)
        return Res(0, stream=stream)

    @rmap.register_request('/post/new_post')
    @permission_control(['post_write'])
    @Arg()
    def new_post(uuid, content, type, privacy='inherit'):
        postid = core.postlib.new_post(
            uuid=uuid, content=content, posttype=type, privacy=privacy)
        if not postid:
            return Res(-114)
        return Res(0, postid=postid)

    @rmap.register_request('/post/delete_post')
    @permission_control(['post_write'])
    @Arg(postid=utils.AutoArgValidators.validate_post_existance)
    def delete_post(uuid, postid):
        post = core.postlib.get_post_by_postid(postid)
        if post.uuid.lower() == uuid:
            post.delete()
            return Res(0)
        return Res(-120)
