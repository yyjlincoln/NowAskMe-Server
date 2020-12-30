from flask import jsonify

_ExceptionDefinitions = {
    10000: 'Development mode',
    0: 'Success',
    -1: 'Request failed.',
    -10001: 'Argument {argument} was not supplied.',
    -10002: 'Conversion for {argument} could not be completed.',
    -100: 'Authentication failed.',
    -101: 'Authentication can not be completed as no login request was initiated.',
    -102: 'The OTP has expired.',
    -103: 'Incorrect OTP.',
    -104: 'Maximum attempts reached. Please request for another OTP.',
    -105: 'User {email} not registered.',
    -106: 'User {email} had already registered. Please log in instead of sign up.',
    -107: 'Authentication is required, however we could not find any credentials.',
    -108: 'Invalid token.',
    -109: 'Token has expired.',
    -110: 'Unknown scope {scope}',
    -111: 'Access to this API is denied. Missing permission: {scope}',
    -112: 'uuid may not be updated',
    -113:'Properties validation failed',
    -114:'Could not commit changes to the database',
}

# Client-side exception bouncing


def Res(code, message=None, **kw):
    if message:
        return jsonify({**{
            'code': code,
            'message': message
        }, **kw})
    if code in _ExceptionDefinitions:
        message = _ExceptionDefinitions[code]
        for key in kw:
            # Plug the variables in
            message = message.replace('{'+key+'}', str(kw[key]))
        return jsonify({**{
            'code': code,
            'message': message
        }, **kw})
    return jsonify({**{
        'code': code
    }, **kw})
