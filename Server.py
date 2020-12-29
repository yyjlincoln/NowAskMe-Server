import views.auth
from flask import Flask, Blueprint
from flask_cors import CORS
from utils.RequestMapping import RequestMap
from utils.AutoArguments import Arg
from utils.ResponseModule import Res
from flask_mongoengine import MongoEngine
from credentials import Credentials

app = Flask(__name__)
rmap = RequestMap()
# CORS Policy
CORS(app)

# Connection to the database
db = MongoEngine()
app.config['MONGODB_SETTINGS'] = {
    "db": "nowaskme",
    "host": "localhost",
    "port": 27017
}
db.init_app(app)

# Import and attach modules
import views.auth
views.auth.attach(rmap)

# Handle flask
rmap.handle_flask(app)



if __name__ == "__main__":
    app.run()
