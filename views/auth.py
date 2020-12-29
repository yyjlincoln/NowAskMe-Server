import datetime
from utils.AutoArguments import Arg
import core.authlib
from utils.ResponseModule import Res


def attach(rmap):

    @rmap.register_request('/auth/check_email')
    @Arg()
    def check_email(email):
        return Res(0, exist=core.authlib.get_if_email_exists(email=email))

    @rmap.register_request('/auth/request_login')
    @Arg()
    def send_email(email):
        sendstatus = core.emaillib.send_login_verification()
        return Res(0,sent=sendstatus)
