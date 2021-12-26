import json
import os
import logging
from commons import CredentialsError


if not os.path.exists('credentials.json'):
    logging.fatal('Could not find credentials.json!')
    raise CredentialsError('Could not load credentials: could not find credentials.json!')

try:
    with open('credentials.json','r') as f:
        Credentials = json.loads(f.read())
except Exception:
    logging.fatal('Could not load credentials!')
    raise CredentialsError('Could not load credentials')

# Read values from Credentials