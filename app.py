import os
import configparser
from routes.auth_routes import auth_bp
from database.database import *
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
config = configparser.ConfigParser()
ini_path = config.read(os.path.abspath(os.path.join("config.ini")))
print(f"INI File Path: {ini_path}")
print(f"Config Sections: {config.sections()}")
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

app.register_blueprint(auth_bp, url_prefix="/auth")


app.config['URI'] = config['PROD']['DB_URI']
print(f"URI: {app.config['URI']}")
app.run()

@app.teardown_appcontext
def teardown_db(exception):
    close_db()