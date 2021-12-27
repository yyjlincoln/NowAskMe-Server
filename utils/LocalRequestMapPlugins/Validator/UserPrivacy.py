import core.privacylib
import core.postlib
import core.userlib
from ...RequestMap.Validators.ValidatorBase import StandardValidator
from ...RequestMap.Exceptions import ValidationError


class UserPrivacyError(ValidationError):
    def __init__(self, code, message=None, **kw):
        super().__init__(code, message)
        self.__dict__.update(kw)


class UserPrivacyValidator(StandardValidator):
    def __init__(self):
        '''
        Use the field `privacy` in endpoint['metadata'] to specify whether the privacy check should be enabled.
        Defaults to False.
        '''
        self.map = None
        self.name = None

    def getEvaluationMethod(self, endpoint, protocol):
        '''
        Returns the evaluation method for the given endpoint.
        '''
        def evaluate():
            'This is currently handled in the view function. In the future, this will be handled here.'
            return
        return evaluate
