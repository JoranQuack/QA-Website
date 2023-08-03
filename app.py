"""root of backend"""
import os
from flask import Flask, render_template
import routes_public
import routes_admin
from functions import image_clean, create_owner, users_clean
from environments import SECRET_KEY
from constants import UPLOAD_FOLDER, MAX_CONTENT_PATH, UPLOAD_EXTENSIONS, DEBUG_MODE


app = Flask(__name__, template_folder="templates")
app.secret_key = SECRET_KEY

app.register_blueprint(routes_public.api, url_prefix="/")
app.register_blueprint(routes_admin.api, url_prefix="/admin")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = MAX_CONTENT_PATH
app.config['UPLOAD_EXTENSIONS'] = UPLOAD_EXTENSIONS


@app.before_first_request
def start_up():
    """runs on app startup"""
    image_clean()
    users_clean()
    create_owner()


@app.errorhandler(404)
def page_not_found(error: str):
    """404 errors"""
    name, message = str(error).split(':')
    return render_template('error.html', name=name, message=message), 404


@app.errorhandler(500)
def application_error(error: str):
    """500 errors"""
    name, message = str(error).split(':')
    return render_template('error.html', name=name, message=message), 500


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=port)
