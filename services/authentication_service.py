from sqlite3 import IntegrityError

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import update

from database.database import get_db


class AuthenticationService:
    def __init__(self, User):
        self.db = None
        self.User = User

    def register(self, email, password):
        try:
            if not email or not password :
                return 400
            self.db = get_db()
            if self.db.query(self.User).filter_by(email=email).first():
                return 409

            hashed_password = generate_password_hash(password)

            new_user = self.User(email=email, password=hashed_password, logged_in=False)

            self.db.add(new_user)
            self.db.commit()

            return  201
        except IntegrityError:
            self.db.rollback()
            return  409
        except Exception as e:
            self.db.rollback()
            return 500

    def login(self, email, password):
        try:
            if not email or not password:
                return  400
            self.db = get_db()
            user = self.db.query(self.User).filter_by(email=email).first()

            if not user:
                return 401

            if not check_password_hash(user.password, password):
                return 401

            self.db.execute(update(self.User).where(self.User.email == email).values(logged_in=True))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            current_app.logger.error(e)
            return 500

        return 200

    def logout(self, email):
        try:

            if not email:
                return 400
            self.db = get_db()
            user = self.db.query(self.User).filter_by(email=email).first()

            if not user or not user.logged_in:
                return 400

            self.db.execute(update(self.User).where(self.User.email == email).values(logged_in=False))
            self.db.commit()

            return 200

        except Exception as e:
            self.db.rollback()
            current_app.logger.error(e)
            return 500
