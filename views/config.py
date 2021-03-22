from utils.AutoArguments import Arg
from utils.ResponseModule import Res
import core.authlib
import core.configlib


def attach(rmap):
    @rmap.register_request('/config')
    @Arg(uuid=str, token=str)
    def configuration_distribution(uuid='', token=''):
        status = 0
        if not core.authlib.get_token_validity(uuid, token):
            uuid = ''
            status = 106

        # Get config using uuid
        return Res(status, config = core.configlib.get_config_by_uuid(uuid))
