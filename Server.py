# Import View Functions
import views.auth
import views.user
import views.post
import views.config
from GlobalContext import API, FlaskProtocolInstance

app = FlaskProtocolInstance.app  # Exposes the Flask app instance to Gunicorn

API.start()
app.run(port=8080)
