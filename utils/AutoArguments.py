import inspect
import commons
from flask import request
from functools import wraps
from utils.ResponseModule import Res

# Construct a decorator to automatically retrieve arguments from a HTTP request


def FlaskRequest(key):
    return request.values.get(key)


def Arg(FetchValues=FlaskRequest, **TypeConvertionFunction):
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


        # @wraps(func)  # Wrap the function so the decorator will not be identified
        # The function is not wrapped such that RequestMapping can detect there is **kw, so it will pass on __fetch_values and __channel
        def __retrieveWrap(*args, **kw):

            # Compatibility layer with RequestMapping.
            # This allows AutoArguments to detect whether this request is from RequestMapping, and if it is, then use __fetch_values instead of default FetchValues().
            if '__fetch_values' in kw:
                FetchValues = kw['__fetch_values']
            # End compatibility layer.

            callDict = {}

            for arg in positional:
                # Check if val is already in kw, as flask may pass some args
                if arg in kw:
                    val = arg[kw]
                else:
                    val = FetchValues(arg)

                if val == None:
                    # A positional argument does not exist - bounce back with error message
                    return Res(-10001, argument=arg)
                callDict[arg] = val

            for arg in keywords:
                val = FetchValues(arg)

                if val != None:
                    # If the value is supplied, use supplied.
                    callDict[arg] = val
                else:
                    # Use default values
                    callDict[arg] = keywords[arg]

            # Now, all required arguments are in callDict. Check and convert them
            for arg in callDict:
                if arg in TypeConvertionFunction:
                    try:
                        # Attempt to convert it
                        callDict[arg] = TypeConvertionFunction[arg](
                            callDict[arg])
                    except:
                        return Res(-10002, argument=arg)

            return func(*args, **callDict)
        return __retrieveWrap
    return _retrieveWrap
