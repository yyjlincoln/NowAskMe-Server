# Import View Functions
import views.auth
import views.user
import views.post
import views.config
from Global import API, FlaskProtocolInstance

from flask_cors import CORS

app = FlaskProtocolInstance.app  # Exposes the Flask app instance to Gunicorn

CORS(app)

API.start()
app.run(port=8080)
