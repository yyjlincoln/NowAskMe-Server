from flask import jsonify
from flask import request
# import json

batch_endpoints = [
    # A list of flask endpoints that, when in that context, 
    # and if __skip_batch is set to true, then return the data
    # in dict form.
    # This is useful as the original form can then be jsonified
    # together with other data.
    '/batch'
]

_ExceptionDefinitions = {
    10000: 'Development mode',
    101: 'Already following.',
    102: 'Already not following.',
    103: 'Already pinned',
    104: 'Already unpinned',
    105: 'Not authenticated yet',
    106:'Insufficient permissions. Requesting as an anomonyous user.',
    0: 'Success',
    -1: 'Request failed.',
    -10001: 'Argument {argument} was not supplied.',
    -10002: 'Conversion for {argument} could not be completed.',
    -20001: 'RequestMap could not map the route {route} to a valid endpoint.',
    -100: 'Authentication failed.',
    -101: 'Authentication can not be completed as no login request was initiated.',
    -102: 'The OTP has expired.',
    -103: 'Incorrect OTP.',
    -104: 'Maximum attempts reached. Please request for another OTP.',
    -105: 'User does not exist.',
    -106: 'User {email} had already registered. Please log in instead of sign up.',
    -107: 'Authentication is required, however we could not find any credentials.',
    -108: 'Invalid token.',
    -109: 'Token has expired.',
    -110: 'Unknown scope {scope}',
    -111: 'Access to this API is denied. Missing permission: {scope}',
    -112: 'uuid may not be updated',
    -113: 'Properties validation failed',
    -114: 'Could not commit changes to the database',
    -115: 'QR login request not found',
    -116: 'QR login request has expired',
    -117: 'QR login request has been rejected',
    -118: 'The requested post {postid} does not exist',
    -119: 'Access to this content is denied.',
    -120: 'Access to this operation has been denied.'
}

# Client-side exception bouncing


def _transparent_data_proxy(data):
    return data


def Res(code, message=None, __skip_batch=True, **kw):

    _jsonify = jsonify
    # Compatibility Layer - Determine whether this is a batch request.
    # If this is a batch request, do NOT jsonify the data; instead,
    # return it as its original form so it will be jsonified later.
    if __skip_batch:
        if request.path in batch_endpoints:
            _jsonify = _transparent_data_proxy

    if message:
        return _jsonify({**{
            'code': code,
            'message': message
        }, **kw})
    if code in _ExceptionDefinitions:
        message = _ExceptionDefinitions[code]
        for key in kw:
            # Plug the variables in
            message = message.replace('{'+key+'}', str(kw[key]))
        return _jsonify({**{
            'code': code,
            'message': message
        }, **kw})
    return _jsonify({**{
        'code': code
    }, **kw})
