"""root of backend"""
import os
from flask import Flask
import routes_frontend
import routes_backend
from environments import SECRET_KEY


app = Flask(__name__, template_folder="templates")
app.secret_key = SECRET_KEY

app.register_blueprint(routes_frontend.api, url_prefix="/")
app.register_blueprint(routes_backend.api, url_prefix="/api")


UPLOAD_FOLDER = 'static/images/'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
