from utils.AutoArguments import Arg
from utils.AutoAuthentication import permission_control
from utils.ResponseModule import Res
import utils.AutoArgValidators
import core.postlib
import utils.PrivacyControl

import time


def attach(rmap):
    @rmap.register_request('/post/get_post')
    @permission_control(['post_view'], checks=['post_privacy'])
    @Arg(postid=utils.AutoArgValidators.validate_post_existance)
    def post_get_post(uuid, postid):
        'Gets post by postid.'
        # Postid has been validated and exists
        if not utils.PrivacyControl.post_privacy(postid, accessFrom=uuid):
            return Res()
        
        pass

    @rmap.register_request('/post/get_user_post')
    @permission_control(['post_view'])
    def post_get_user_post():
        pass

    @rmap.register_request('/post/get_stream')
    @permission_control(['post_view'])
    def post_get_stream():
        pass
