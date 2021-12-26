import core.authlib
import core.email
from Global import API


@API.endpoint('check-email', {
    'scopes': [],
    'httproute': '/auth/check_email'
})
def check_email(email, makeResponse):
    return makeResponse(0, exist=core.authlib.get_if_email_exists(email=email))


@API.endpoint('send-email', {
    'scopes': [],
    'httproute': '/auth/send_email'
})
def send_email(email, makeResponse):
    uuid = core.authlib.get_uuid_by_email(email)
    name = email
    if uuid:
        userinfo = core.userlib.get_user_info_by_uuid(uuid)
        if userinfo.name != 'user':
            name = userinfo.name

    code = core.email.send_login_verification(email=email, name=name)

    if code is False:
        return makeResponse(-1, message='Could not send the email!', sent=False)
    return makeResponse(0, sent='True')


@API.endpoint('login-via-email', {
    'scopes': [],
    'httproute': '/auth/login/email'
})
def login_via_email(email, otp, makeResponse, scope='login'):
    code = core.authlib.email_verification(email, otp)
    if code == 0:
        uuid = core.authlib.get_uuid_by_email(email)
        if not uuid:
            return makeResponse(-105, email=email)
        token = core.authlib.new_token(uuid=uuid, scope=scope)
        user = core.userlib.get_user_info_by_uuid(uuid=uuid)
        return makeResponse(0, 'Successfully logged in.', token=token, userid=user.userid, name=user.name, uuid=uuid)

    return makeResponse(code, email=email)


@API.endpoint('register', {
    'scopes': [],
    'httproute': '/auth/register'
})
def register(email, otp, makeResponse):
    code = core.authlib.email_verification(email, otp)
    if code == 0:
        uuid = core.authlib.get_uuid_by_email(email)
        if uuid:
            return makeResponse(-106, email=email)
        uuid = core.authlib.new_user(email)
        if not uuid:
            return makeResponse(-106, email=email)
        token = core.authlib.new_token(uuid=uuid, scope='login')
        user = core.userlib.get_user_info_by_uuid(uuid=uuid)
        core.email.send_welcome_email(uuid)
        return makeResponse(0, 'Successfully registered.', token=token, userid=user.userid, name=user.name, uuid=uuid)
    return makeResponse(code, email=email)


@API.endpoint('check_scope', {
    'scopes': ['basic_view'],
    'httproute': '/auth/check_scope'
})
def check_scope(uuid, token, makeResponse):
    return makeResponse(0, scope=core.authlib.get_token_scope(uuid, token))
