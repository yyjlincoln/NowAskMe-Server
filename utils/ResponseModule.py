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
    -105: 'User {email} not registered.'
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
