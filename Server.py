from flask import Flask, Blueprint
from flask_cors import CORS
from views.auth import app as AuthBluePrint
from views.devtest import app as DevtestBluePrint
from utils import RequestMapping
app = Flask(__name__)
CORS(app)


# Compile Request
if __name__=="__main__":
    app.run()