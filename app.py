# import os
# import configparser
# from routes.auth_routes import auth_bp
# from database.database import *
# from flask import Flask
#
# from routes.crud_song_routes import crud_bp
# from routes.prediction_routes import prediction_bp
#
# config = configparser.ConfigParser()
# ini_path = config.read(os.path.abspath(os.path.join("config.ini")))
# print(f"INI File Path: {ini_path}")
# print(f"Config Sections: {config.sections()}")
# app = Flask(__name__)
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
# app.register_blueprint(auth_bp, url_prefix="/auth")
# app.register_blueprint(crud_bp, url_prefix="/crud")
# app.register_blueprint(prediction_bp, url_prefix="/ai")
# app.config['URI'] = config['PROD']['DB_URI']
# app.config["SECRET_KEY"] = "KO2NQ-bA0VDXhaUH3_Qew1oqT8PZGRx6HSWeJgrFLlVzx4ue3rxhtRrnjEWNj-qHPWyQ4YQ-6b2fm_K59h7wsA"
#
# print(f"URI: {app.config['URI']}")
# db_singleton = DatabaseSingleton(app)
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
#
#
# @app.teardown_appcontext
# def teardown_db(exception):
#     close_db()



import os
import configparser
from flask import Flask

from routes.auth_routes import auth_bp
from routes.crud_song_routes import crud_bp
from routes.prediction_routes import prediction_bp
from database.database import DatabaseSingleton, close_db

def create_app(testing=False):
    app = Flask(__name__)

    config = configparser.ConfigParser()
    ini_path = config.read(os.path.abspath(os.path.join("config.ini")))
    print(f"INI File Path: {ini_path}")
    print(f"Config Sections: {config.sections()}")

    if testing:

        app.config['URI'] = "sqlite:///:memory:"
        app.config["TESTING"] = True
    else:
        app.config['URI'] = config['PROD']['DB_URI']

    app.config["SECRET_KEY"] = "KO2NQ-bA0VDXhaUH3_Qew1oqT8PZGRx6HSWeJgrFLlVzx4ue3rxhtRrnjEWNj-qHPWyQ4YQ-6b2fm_K59h7wsA"
    print(f"URI: {app.config['URI']}")

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(crud_bp, url_prefix="/crud")
    app.register_blueprint(prediction_bp, url_prefix="/ai")

    db_singleton = DatabaseSingleton(app)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
