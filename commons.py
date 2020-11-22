# Exceptions
class NAMExceptions(Exception):
    pass

class CallbackFunctionNotCallableException(NAMExceptions):
    'The callback function is not callable.'