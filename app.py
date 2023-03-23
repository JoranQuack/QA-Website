# pylint: disable=import-error
"""root of backend"""
import os
from flask import Flask
from routes import api
from environments import SECRET_KEY


app = Flask(__name__, template_folder="templates")
app.secret_key = SECRET_KEY

app.register_blueprint(api, url_prefix="/")

UPLOAD_FOLDER = 'static/images/'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
