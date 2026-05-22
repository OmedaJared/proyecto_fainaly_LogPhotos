from flask import Flask
from config import Config
from routes import auth, files

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='../static'
)
app.config.from_object(Config)

app.register_blueprint(auth.auth_bp)
app.register_blueprint(files.files_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)