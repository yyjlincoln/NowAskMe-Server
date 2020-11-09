from flask import Blueprint, request
import datetime
from utils import Arg

app = Blueprint('vauth', __name__)

@app.route('/')
@Arg()
def test(testPositional, testArguments = 'Test Default'):
    return 'ok'