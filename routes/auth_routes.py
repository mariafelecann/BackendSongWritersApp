from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from database.database import *
from sqlalchemy import update

from services.authentication_service import AuthenticationService

auth_bp = Blueprint("auth", __name__)

authentication_service = AuthenticationService(User, Song)
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        response, code = authentication_service.login(email, password)
        return jsonify(response), code


    except Exception as e:
        db.rollback()
        return jsonify({"error": "database error", "details": str(e)}), 500


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        code = authentication_service.register(email,password)
        if code == 201:
            return jsonify({"message": "registration successful"}), 201
        else:
            if code == 409:
                return jsonify({"error": "email already registered"}), 409
            else:
                if code == 400:
                    return jsonify({"error": "email, password, and username are required"}), 400
                else:
                    if code == 500:
                        return jsonify({"error": "database error"}), 500

    except IntegrityError:
        db.rollback()
        return jsonify({"error": "email already registered"}), 409
    except Exception as e:
        db.rollback()
        return jsonify({"error": "database error", "details": str(e)}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    try:
        data = request.get_json()
        email = data.get("email")
        code = authentication_service.logout(email)
        if code == 200:
            return jsonify({"message": "successfully logged out"}), 200

        else:
            if code == 400:
                return jsonify({"error": "email is required or user is not logged in"}), 400
            else:
                if code == 500:
                    return jsonify({"error": "database error"}), 500

    except Exception as e:
        db.rollback()
        return jsonify({"error": "logout failed", "details": str(e)}), 500


@auth_bp.route("/delete_account", methods=["POST"])
def delete_account():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        code = authentication_service.delete_account(email, password)

        if code == 200:
            return jsonify({"message": "account successfully deleted"}), 200
        elif code == 400:
            return jsonify({"error": "email and password are required"}), 400
        elif code == 404:
            return jsonify({"error": "user not found"}), 404
        elif code == 401:
            return jsonify({"error": "invalid password"}), 401
        else:
            return jsonify({"error": "database error"}), 500

    except Exception as e:
        return jsonify({"error": "error while deleting account", "details": str(e)}), 500
