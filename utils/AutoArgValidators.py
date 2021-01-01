import core.userlib
from utils.AutoArguments import ReturnRaw
from utils.ResponseModule import Res

def validate_user_existance(uuid):
    'The provided uuid must be associated with an existing user. If it is, return the uuid; otherwise, raise an exception.'
    if uuid:
        if core.userlib.get_user_info_by_uuid(uuid):
            return uuid
        raise ReturnRaw(Res(-105, uuid=uuid, email=uuid))
