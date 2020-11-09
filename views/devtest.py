from flask import Blueprint
from utils.AutoArguments import Arg
from utils.ResponseModule import Res

app = Blueprint('devtest', __name__)


@app.route('/dev/addition')
@Arg(a=float, b=float,donotbounce=bool)
def dev_addition(a, b,donotbounce=False):
    if donotbounce:
        return str(a+b)
    else:
        return Res(10000)
