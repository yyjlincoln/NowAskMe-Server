from flask import Flask, Blueprint
from flask_cors import CORS
from views.auth import app as AuthBluePrint
from views.devtest import app as DevtestBluePrint
app = Flask(__name__)
CORS(app)

app.register_blueprint(AuthBluePrint)
app.register_blueprint(DevtestBluePrint)


if __name__=="__main__":
    app.run()