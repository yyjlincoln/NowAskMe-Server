from ...RequestMap.Validators.ValidatorBase import StandardValidator
from ...RequestMap.Exceptions import ValidationError
import core.authlib

# Token Type -- Granted Scopes
scopeList = {
    'login': [
        'update_profile',
        'basic_view',
        'basic_write',
        'renew_token',
        'post_view',
        'post_write',
        'relation_view',
        'relation_write'
    ],
    'expired': {},
}


class AuthenticationError(ValidationError):
    def __init__(self, code, message=None, **kw):
        super().__init__(code, message)
        self.__dict__.update(kw)


class AuthenticationValidator(StandardValidator):
    def __init__(self):
        '''
        Use the field `scopes` (list[str]) in endpoint['metadata'] to specify the required scopes.
        Defaults to be ['basic_view', 'baisc_write'].

        To mark an endpoint as public, set the scope to be [].
        '''
        self.map = None
        self.name = None

    def initialise(self):
        'Initialise the validator - there is nothing to initialise.'
        pass

    def getEvaluationMethod(self, endpoint, protocol):
        '''
        Returns the evaluation method for the given endpoint.
        '''
        requiredScopes = endpoint['metadata'].get(
            'scopes', ['basic_view', 'basic_write'])

        def evaluate(uuid=None, token=None):
            # RequestMap extracts uuid and token for us so it becomes easier to use.
            # They are not optional though.

            if requiredScopes != []:
                if not uuid or not token:
                    raise AuthenticationError(-107)

                tokenScope = core.authlib.get_token_scope(uuid, token)
                if not tokenScope:
                    raise AuthenticationError(-108)

                if tokenScope == 'expired':
                    raise AuthenticationError(-109)

                if tokenScope not in scopeList:
                    raise AuthenticationError(-110, scope=tokenScope)

                for requiredScope in requiredScopes:  # For all required scopes
                    # If the current scope group does not satisfy all scopes
                    if requiredScope not in scopeList[tokenScope]:
                        return AuthenticationError(-111, scope=requiredScope)

        return evaluate
