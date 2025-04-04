from flask import current_app, g
from sqlalchemy import create_engine, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from werkzeug.local import LocalProxy

# Define your SQLAlchemy models
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#
#     email = Column(String)
#     password = Column(String)
#     logged_in = Column(Boolean)
#
# # class Song(Base):
# #     __tablename__ = 'songs'
# #     id = Column(Integer, primary_key=True)
# #     title = Column(String)
# #     artist = Column(String)
#
# def get_db():
#     db = getattr(g, "_database", None)
#     if db is None:
#         DATABASE_URL = current_app.config.get("URI")
#         if not DATABASE_URL:
#             print("SUPABASE_URI not configured")
#             return None
#
#         try:
#             engine = create_engine(DATABASE_URL)
#             Base.metadata.create_all(engine)
#             Session = scoped_session(sessionmaker(bind=engine))
#             db = Session()
#             setattr(g, "_database", db)
#
#             print("Successfully connected to Supabase!")
#
#         except Exception as e:
#             print(f"Error connecting to Supabase: {e}")
#             return None
#
#     return db
#
# def close_db(e=None):
#     db = getattr(g, "_database", None)
#     if db is not None:
#         db.close()
#
# db = LocalProxy(get_db)

# Example usage in a Flask app:
# app.config['SUPABASE_URI'] = "your_supabase_connection_string"
# @app.teardown_appcontext
# def teardown_db(exception):
#     close_db()
# @app.route('/users')
# def get_users():
#     session = db
#     users = session.query(User).all()
#     user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
#     return jsonify(user_list)


from flask import current_app, g
from sqlalchemy import create_engine, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from werkzeug.local import LocalProxy

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    logged_in = Column(Boolean)

class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    email = Column(String, ForeignKey('users.email'))
    lyrics = Column(String)
    genre = Column(String)

class DatabaseSingleton:
    _instance = None

    def __new__(cls, app=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = None
            cls._instance.Session = None
            cls._instance.app = app

            if app:
                cls._instance.init_app(app)

        return cls._instance

    def init_app(self, app):
        if self.engine is None:
            DATABASE_URL = app.config.get("URI")
            if not DATABASE_URL:
                print("SUPABASE_URI not configured")
                return

            try:
                self.engine = create_engine(DATABASE_URL)
                Base.metadata.create_all(self.engine)
                self.Session = scoped_session(sessionmaker(bind=self.engine))

                print("Successfully connected to Supabase!")

            except Exception as e:
                print(f"Error connecting to Supabase: {e}")

    def get_session(self):
        if self.Session is None:

          if self.app is None:
            return None
          self.init_app(self.app)
        return self.Session()

def get_db():
    db_singleton = DatabaseSingleton(current_app)
    db = getattr(g, "_database", None)

    if db is None:
        db = db_singleton.get_session()
        setattr(g, "_database", db)

    return db

def close_db(e=None):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

db = LocalProxy(get_db)

# Example usage in a Flask app:
# app.config['SUPABASE_URI'] = "your_supabase_connection_string"
# @app.teardown_appcontext
# def teardown_db(exception):
#     close_db()
# @app.route('/users')
# def get_users():
#     session = db
#     users = session.query(User).all()
#     user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
#     return jsonify(user_list)