import core.userlib

PUBLIC_CONFIG = {
    'ui.login.showOtherOptions': True,
    'ui.login.showQR': False,
    'ui.login.showPassword': False,
    'ui.showDashboard': True,
    'ui.showFriends': True,
    'ui.showBox': False,
    'ui.showStream': True,
    'ui.showMe': True,
    'ui.showSettings': False,
    'ui.profile.showQA': False,
    'beta': False
}

BETA_CONFIG = {
    'ui.login.showQR': True,
    'ui.login.showPassword': True,
    'ui.showDashboard': True,
    'ui.showFriends': True,
    'ui.showBox': True,
    'ui.showStream': True,
    'ui.showMe': True,
    'ui.showSettings': True,
    'ui.profile.showQA': True,
    'beta': True
}


def get_config_by_uuid(uuid=''):
    if uuid == '':
        return PUBLIC_CONFIG
    if core.userlib.get_beta_status(uuid=uuid) == True:
        return BETA_CONFIG

    return PUBLIC_CONFIG
