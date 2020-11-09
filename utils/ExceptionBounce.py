from flask import jsonify

_ExceptionDefinitions = {
    -10001: 'Argument {argument} was not supplied.',
    -10002: 'Conversion for {argument} could not be completed.'
}

# Client-side exception bouncing
def Bounce(code, message=None, **kw):
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
