import views.auth
import views.user
import views.post
import views.config

from flask import Flask
from utils.RequestMapping import RequestMap
from utils.AutoArguments import Arg
from flask_mongoengine import MongoEngine
import json

app = Flask(__name__)
# Since Arg() will have to be wrapped in order to allow Flask to work,
# And that will result the param detection to detect the ORIGINAL function
# NOT the Arg() function, then __fetch_values will NOT be passed.
# To resolve this, enable this option so it forcibly passes the arguments.
rmap = RequestMap(always_pass_channel_and_fetch_values=True)


# Import and attach modules
views.auth.attach(rmap)
views.user.attach(rmap)
views.post.attach(rmap)
views.config.attach(rmap)

# Handle flask
rmap.handle_flask(app)


@app.route('/batch', methods=['GET', 'POST'])
@Arg(batch=json.loads)
def batch_request(batch):
    return rmap.parse_batch(batch)


if __name__ == "__main__":
    app.run(port=5001)
