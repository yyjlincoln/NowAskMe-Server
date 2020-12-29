from flask import Flask, Blueprint
from flask_cors import CORS
from utils.RequestMapping import RequestMap
from utils.AutoArguments import Arg
from utils.ResponseModule import Res

import views.auth
import views.devtest

app = Flask(__name__)
rmap = RequestMap()
CORS(app)

@rmap.register_request('/')
@Arg(a=float,b=float,c=float)
def addition(a,b,c=1.5):
    return Res(0, 'ok', result=(a+b)*c)


rmap.handle_flask(app)


if __name__ == "__main__":
    app.run()
