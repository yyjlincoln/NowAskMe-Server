from flask import Flask, Blueprint
from flask_cors import CORS
from utils.RequestMapping import RequestMap
from utils.AutoArguments import Arg

import views.auth
import views.devtest

app = Flask(__name__)
CORS(app)


rmap = RequestMap()

@rmap.register_request('/')
@Arg()
def addition(__fetch_values):
    return __fetch_values('hello')

rmap.handle_flask(app)


if __name__ == "__main__":
    app.run()
