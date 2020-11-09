from flask import Flask, Blueprint
from flask_cors import CORS
from views.auth import app as AuthBluePrint

app = Flask(__name__)
CORS(app)

app.register_blueprint(AuthBluePrint)

app.run()