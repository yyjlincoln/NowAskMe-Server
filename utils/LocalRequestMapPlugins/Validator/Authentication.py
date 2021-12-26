from ...RequestMap.Validators.ValidatorBase import StandardValidator
from ...RequestMap.Exceptions import ValidationError


class AuthenticationValidator(StandardValidator):
    def __init__(self):
        '''
        Use the field `authlevel` in endpoint['metadata'] to specify the required auth level.
        '''
        self.map = None
        self.name = None

    def initialise(self):
        pass

    def getEvaluationMethod(self, endpoint, protocolName):
        '''
        Returns the evaluation method for the given endpoint.
        The return value is discarded. Throw an error if validation fails.
        Preferably the error should be an instance of ValidationError.
        '''
        def evaluate(sampleValidatorArgument):  # Put required/optional arguments here
            raise ValidationError(-400, 'Not implemented. Can not validate.')
        return evaluate
