import core.authlib
import core.configlib
from GlobalContext import API


@API.endpoint('get-config', {
    'scopes': [],
    'httproute': '/config/get_config'
}, uuid=str, token=str)
def configuration_distribution(makeResponse, uuid='', token=''):
    status = 0
    if not core.authlib.get_token_validity(uuid, token):
        uuid = ''
        status = 106

    # Get config using uuid
    return makeResponse(status, config=core.configlib.get_config_by_uuid(uuid))
