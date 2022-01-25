from mongoengine import connect
from utils.RequestMap import Map
from utils.RequestMap.Protocols.Flask import HTTPViaFlask
from utils.RequestMap.Response.JSON import JSONStandardizer
from utils.LocalRequestMapPlugins.Validator import AuthenticationValidator, UserPrivacyValidator

API = Map()

# This is seperately declared so that the Flask app instance is accessible to Gunicorn
FlaskProtocolInstance = HTTPViaFlask()

API.useProtocol(FlaskProtocolInstance)
API.useResponseHandler(JSONStandardizer({
    10000: 'Development mode',
    101: 'Already following.',
    102: 'Already not following.',
    103: 'Already pinned',
    104: 'Already unpinned',
    105: 'Not authenticated yet',
    106: 'Insufficient permissions. Requesting as an anomonyous user.',
    0: 'Success',
    -1: 'Request failed.',
    -10001: 'Not all arguments were not supplied.',
    -10002: 'Conversion for argument could not be completed.',
    -20001: 'RequestMap could not map the route to a valid endpoint.',
    -100: 'Authentication failed.',
    -101: 'Authentication can not be completed as no login request was initiated.',
    -102: 'The OTP has expired.',
    -103: 'Incorrect OTP.',
    -104: 'Maximum attempts reached. Please request for another OTP.',
    -105: 'User does not exist.',
    -106: 'User email had already registered. Please log in instead of sign up.',
    -107: 'Authentication is required, however we could not find any credentials.',
    -108: 'Invalid token.',
    -109: 'Token has expired.',
    -110: 'Unknown scope.',
    -111: 'Access to this API is denied. Missing scope.',
    -112: 'uuid may not be updated',
    -113: 'Properties validation failed',
    -114: 'Could not commit changes to the database',
    -115: 'QR login request not found',
    -116: 'QR login request has expired',
    -117: 'QR login request has been rejected',
    -118: 'The requested post does not exist',
    -119: 'Access to this content is denied.',
    -120: 'Access to this operation has been denied.'
}))
API.useValidator(AuthenticationValidator())
API.useValidator(UserPrivacyValidator())

# Connect to the database
import json
with open("credentials.json", "r") as f:
    secrets = json.load(f)
    assert 'dbURL' in secrets
    connect(host=secrets['dbURL'])
