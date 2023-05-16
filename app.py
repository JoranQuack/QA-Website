"""root of backend"""
import os
from flask import Flask, render_template
import routes_public
import routes_admin
from environments import SECRET_KEY


app = Flask(__name__, template_folder="templates")
app.secret_key = SECRET_KEY

app.register_blueprint(routes_public.api, url_prefix="/")
app.register_blueprint(routes_admin.api, url_prefix="/admin")

app.config['UPLOAD_FOLDER'] = 'static/images/uploaded'
app.config['MAX_CONTENT_PATH'] = 16000000
app.config['UPLOAD_EXTENSIONS'] = ['.jpeg', '.jpg', '.png', '.gif', '.JPG']


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
    app.run(debug=True, host='0.0.0.0', port=port)
