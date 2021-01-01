# Exceptions
class NAMExceptions(Exception):
    pass

class CallbackFunctionNotCallableException(NAMExceptions):
    'The callback function is not callable.'

class CredentialsError(NAMExceptions):
    'Could not load credentials or incorrect credentials'

class ValidationError(NAMExceptions):
    'Validation error.'