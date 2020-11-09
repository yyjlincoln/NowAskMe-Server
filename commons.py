# Exceptions
class GroupsExceptions(Exception):
    pass

class CallbackFunctionNotCallableException(GroupsExceptions):
    'The callback function is not callable.'