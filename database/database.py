
from sqlalchemy import create_engine, Boolean, ForeignKey

from flask import current_app, g
from sqlalchemy import create_engine, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import declarative_base
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
                print("Database URI not configured")
                return

            try:
                self.engine = create_engine(DATABASE_URL, echo=False)
                Base.metadata.create_all(self.engine)
                self.Session = scoped_session(sessionmaker(bind=self.engine))
                print(f"Connected to DB at: {DATABASE_URL}")
            except Exception as e:
                print(f"Error connecting to DB: {e}")

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
