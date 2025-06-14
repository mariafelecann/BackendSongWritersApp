
from flask import Blueprint, request, jsonify, current_app

from database.database import Song
from services.crud_service import SongCrudOperationsService

crud_bp = Blueprint("crud", __name__)
crud_service = SongCrudOperationsService(Song)

@crud_bp.route("/add", methods=["POST"])
def add_song():
    data = request.get_json()
    title = data.get("title")
    email = data.get("email")
    genre = data.get("genre")
    lyrics = data.get("lyrics")
    print(title, email, lyrics, genre)
    current_app.logger.info(f"Adding song with title: {title}, email: {email}, genre: {genre}, lyrics: {lyrics}")
    code = crud_service.add_song(title, email, lyrics, genre)
    match code:
        case 200:
            return jsonify({"message":"Song added successfully"}), 200
        case 400:
            return jsonify({"error":"Title, email, lyrics and genre are required"}), 400
        case 409:
            return jsonify({"error":"A song with this title already exists"}), 409
        case 500:
            return jsonify({"error":"Database error"}), 500

@crud_bp.route("/delete", methods=["POST"])
def delete_song():
    data = request.get_json()
    title = data.get("title")
    email = data.get("email")
    code = crud_service.delete_song(title, email)
    match code:
        case 200:
            return jsonify({"message":"song deleted successfully"}), 200
        case 400:
            return jsonify({"error":"title and email are required"}), 400
        case 404:
            return jsonify({"error":"song not found"}), 404
        case 500:
            return jsonify({"error":"database error"}), 500

@crud_bp.route("/songs", methods=["GET"])
def get_songs():
    try:
        email = request.args.get("email")
        if not email:
            return jsonify({"error": "email is required"}), 400
        code, songs_list = crud_service.get_all_songs(email)
        if code == 200:
            return jsonify(songs_list), 200
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"error": "database error"}), 500
