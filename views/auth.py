import datetime
from utils.AutoArguments import Arg
import core.authlib
import core.emaillib
from utils.AutoAuthentication import permission_control
from utils.ResponseModule import Res


def attach(rmap):

    @rmap.register_request('/auth/check_email')
    @Arg()
    def check_email(email):
        return Res(0, exist=core.authlib.get_if_email_exists(email=email))

    @rmap.register_request('/auth/send_email')
    @Arg()
    def send_email(email):
        uuid = core.authlib.get_uuid_by_email(email)
        name = email
        if uuid:
            userinfo = core.authlib.get_user_info_by_uuid(uuid)
            if userinfo.name != 'user':
                name = userinfo.name

        code = core.emaillib.send_login_verification(email=email, name=name)

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
            return Res(0, 'Successfully logged in.', token=token, userid=user.userid, name=user.name, uuid=uuid)

        return Res(code, email=email)

    @rmap.register_request('/auth/register')
    @Arg()
    def register(email, otp):
        code = core.authlib.email_verification(email, otp)
        if code == 0:
            uuid = core.authlib.get_uuid_by_email(email)
            print(uuid)
            if uuid:
                return Res(-106, email=email)
            uuid = core.authlib.new_user(email)
            if not uuid:
                return Res(-106, email=email)
            token = core.authlib.new_token(uuid=uuid, scope='login')
            user = core.authlib.get_user_info_by_uuid(uuid=uuid)
            return Res(0, 'Successfully registered.', token=token, userid=user.userid, name=user.name, uuid=uuid)
        return Res(code, email=email)

    @rmap.register_request('/auth/check_scope')
    @permission_control(scopes=['basic_view'])
    @Arg()
    def check_scope(uuid, token):
        return Res(0, scope=core.authlib.get_token_scope(uuid, token))
