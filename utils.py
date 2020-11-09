import inspect
import commons
from flask import request, jsonify
from functools import wraps


_ExceptionDefinitions = {
    -10001: 'Argument {argument} was not supplied.',
    -10002: 'Conversion for {argument} could not be completed.'
}

# Client-side exception bouncing
def ExceptionBounce(code, message=None, **kw):
    if message:
        return jsonify({
            'code': code,
            'message': message
        })
    if code in _ExceptionDefinitions:
        message = _ExceptionDefinitions[code]
        for key in kw:
            # Plug the variables in
            message = message.replace('{'+key+'}', kw[key])
        return jsonify({
            'code':code,
            'message':message
        })
    return jsonify({
        'code':code
    })


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

        @wraps(func)  # Wrap the function so the decorator will not be identified
        def __retrieveWrap(*args, **kw):
            callDict = {}

            for arg in positional:
                val = request.values.get(arg)
                # Check if val is already in kw, as flask may pass some args
                if arg in kw:
                    val = arg[kw]

                if not val:
                    # A positional argument does not exist - bounce back with error message
                    return ExceptionBounce(-10001, argument = arg)
                callDict[arg] = val

            for arg in keywords:
                val = request.values.get(arg)
                if val:
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
                        callDict[arg] = TypeConvertionFunction[arg](val)
                    except:
                        return ExceptionBounce(-10002, argument=arg)

            return func(*args, **kw, **callDict)
        return __retrieveWrap
    return _retrieveWrap
