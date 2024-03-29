import views.auth
import views.user
import views.post
import views.config

from flask import Flask, Blueprint
from utils.RequestMapping import RequestMap
from utils.AutoArguments import Arg
from utils.ResponseModule import Res
from flask_mongoengine import MongoEngine
from credentials import Credentials
import json

app = Flask(__name__)
# Since Arg() will have to be wrapped in order to allow Flask to work,
# And that will result the param detection to detect the ORIGINAL function
# NOT the Arg() function, then __fetch_values will NOT be passed.
# To resolve this, enable this option so it forcibly passes the arguments.
rmap = RequestMap(always_pass_channel_and_fetch_values=True)

# Connection to the database
db = MongoEngine()
app.config['MONGODB_SETTINGS'] = {
    "db": "nowaskme",
    "host": "localhost",
    "port": 27017
}
db.init_app(app)

# Import and attach modules
views.auth.attach(rmap)
views.user.attach(rmap)
views.post.attach(rmap)
views.config.attach(rmap)

# Handle flask
rmap.handle_flask(app)


@app.route('/batch', methods = ['GET','POST'])
@Arg(batch=json.loads)
def batch_request(batch):
    return rmap.parse_batch(batch)

if __name__ == "__main__":
    app.run(port=5001)
