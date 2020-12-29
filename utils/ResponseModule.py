from flask import jsonify

_ExceptionDefinitions = {
    10000: 'Development mode',
    -1: 'Request failed.',
    -10001: 'Argument {argument} was not supplied.',
    -10002: 'Conversion for {argument} could not be completed.',
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
            message = message.replace('{'+key+'}', kw[key])
        return jsonify({**{
            'code': code,
            'message': message
        }, **kw})
    return jsonify({**{
        'code': code
    }, **kw})
