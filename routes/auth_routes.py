from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from database.database import *
from sqlalchemy import update

from services.authentication_service import AuthenticationService

auth_bp = Blueprint("auth", __name__)

authentication_service = AuthenticationService(User)
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        response, code = authentication_service.login(email, password)
        return jsonify(response), 200



        # if not email or not password:
        #     return jsonify({"error": "Email and password are required"}), 400
        #
        # user = db.query(User).filter_by(email=email).first()
        #
        # if not user:
        #     return jsonify({"error": "Invalid email or password"}), 401
        #
        # if not check_password_hash(user.password, password):
        #     return jsonify({"error": "Invalid email or password"}), 401
        #
        # db.execute(update(User).where(User.email == email).values(logged_in=True))
        # db.commit()
        #
        # return jsonify({"message": "Login successful", "user": {"id": user.id, "email": user.email}}), 200 # changed user return

    except Exception as e:
        db.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        code = authentication_service.register(email,password)
        if code == 201:
            return jsonify({"message": "Registration successful"}), 201
        else:
            if code == 409:
                return jsonify({"error": "Email already registered"}), 409
            else:
                if code == 400:
                    return jsonify({"error": "Email, password, and username are required"}), 400
                else:
                    if code == 500:
                        return jsonify({"error": "Database error"}), 500

        # if not email or not password :
        #     return jsonify({"error": "Email, password, and username are required"}), 400
        #
        # if db.query(User).filter_by(email=email).first():
        #     return jsonify({"error": "Email already registered"}), 409
        #
        # hashed_password = generate_password_hash(password)
        #
        # new_user = User(email=email, password=hashed_password, logged_in=False)
        #
        # db.add(new_user)
        # db.commit()
        #
        # return jsonify({"message": "Registration successful", "user_id": new_user.id}), 201

    except IntegrityError:
        db.rollback()
        return jsonify({"error": "Email already registered"}), 409
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    try:
        data = request.get_json()
        email = data.get("email")
        code = authentication_service.logout(email)
        if code == 200:
            return jsonify({"message": "Successfully logged out"}), 200

        else:
            if code == 400:
                return jsonify({"error": "Email is required or user is not logged in"}), 400
            else:
                if code == 500:
                    return jsonify({"error": "Database error"}), 500
        # if not email:
        #     return jsonify({"error": "Email is required"}), 400
        #
        # user = db.query(User).filter_by(email=email).first()
        #
        # if not user or not user.logged_in:
        #     return jsonify({"error": "User is not logged in"}), 400
        #
        # db.execute(update(User).where(User.email == email).values(logged_in=False))
        # db.commit()
        #
        # return jsonify({"message": "Successfully logged out"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": "Logout failed", "details": str(e)}), 500