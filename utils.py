import inspect
import commons
from flask import request, jsonify
from functools import wraps

# Construct a decorator to automatically retrieve arguments from a HTTP request


def Arg(**TypeConvertionFunction):
    # First run - check type conversion function
    for arg in TypeConvertionFunction:
        if not callable(TypeConvertionFunction[arg]):
            raise commons.CallbackFunctionNotCallableException(
                'Callback function for argument \"'+str(arg)+'\" is invalid as it is not callable.')

    def _retrieveWrap(func):
        # Also first run, but after initialization (got the function), inspect to get the argument.

        inspected = inspect.getfullargspec(func)
        # This gets the positional arguments.
        # defaults is a subset of args, and optional ones (or keywords) are always put the the last.
        # Therefore, we can map it.
        positional = inspected.args[:-len(inspected.defaults)
                                    ] if inspected.defaults else inspected.args
        keywords = dict(
            zip(inspected.args[-len(inspected.defaults):] if inspected.defaults else [], inspected.defaults if inspected.defaults else []))
        # zip the keys and values together, then convert it to a dict

        print(positional, keywords)

        @wraps(func)  # Wrap the function so the decorator will not be identified
        def __retrieveWrap(*args, **kw):
            return func(*args, **kw)
        return __retrieveWrap
    return _retrieveWrap
