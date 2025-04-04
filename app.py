import os
import configparser
from routes.auth_routes import auth_bp
from database.database import *
from flask import Flask

from routes.crud_song_routes import crud_bp
from routes.prediction_routes import prediction_bp

config = configparser.ConfigParser()
ini_path = config.read(os.path.abspath(os.path.join("config.ini")))
print(f"INI File Path: {ini_path}")
print(f"Config Sections: {config.sections()}")
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(crud_bp, url_prefix="/crud")
app.register_blueprint(prediction_bp, url_prefix="/ai")
app.config['URI'] = config['PROD']['DB_URI']
print(f"URI: {app.config['URI']}")
db_singleton = DatabaseSingleton(app)
app.run()

@app.teardown_appcontext
def teardown_db(exception):
    close_db()