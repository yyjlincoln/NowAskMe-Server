import datetime
from utils.AutoArguments import Arg
import core.authlib
import core.emaillib
from utils.ResponseModule import Res


def attach(rmap):

    @rmap.register_request('/auth/check_email')
    @Arg()
    def check_email(email):
        return Res(0, exist=core.authlib.get_if_email_exists(email=email))

    @rmap.register_request('/auth/send_email')
    @Arg()
    def send_email(email):
        code = core.emaillib.send_login_verification(email=email)

        if code == False:
            return Res(-1, sent=False, message='Could not send the email!')
        return Res(0, sent='True')

    @rmap.register_request('/auth/login/email')
    @Arg()
    def login_email(email, otp, scope='login'):
        code = core.authlib.email_verification(email, otp)
        if code == 0:
            uuid = core.authlib.get_uuid_by_email(email)
            if not uuid:
                return Res(-105, email=email)
            token = core.authlib.new_token(uuid=uuid, scope=scope)
            user = core.authlib.get_user_info_by_uuid(uuid=uuid)
            return Res(0, 'Successfully logged in.', token=token, userid=user.userid, name=user.name)

        return Res(code, email=email)

    @rmap.register_request('/auth/register/email')
    @Arg()
    def register_email(email):
        pass
