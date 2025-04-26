from database.database import *


class SongCrudOperationsService:
    def __init__(self, Song):
        self.db = None
        self.Song = Song

    def add_song(self, title, email, lyrics, genre):
        try:
            if not title or not email or not lyrics or not genre:
                return 400
            else:
                db = get_db()
                if db.query(self.Song).filter_by(title = title, email = email).first():
                    return 409
                else:
                    new_song = Song(title=title, email=email, lyrics=lyrics, genre=genre)
                    db.add(new_song)
                    db.commit()
                    return 200
        except Exception as e:
            db.rollback()
            current_app.logger.error(e)
            return 500

    def delete_song(self, title, email):
        try:
            if not title or not email:
                return 400
            else:
                db = get_db()
                song = db.query(self.Song).filter_by(title = title, email = email).first()
                if not song:
                    return 404
                db.delete(song)
                db.commit()
                return 200
        except Exception as e:
            db.rollback()
            current_app.logger.error(e)
            return 500

    def get_all_songs(self, email):
        try:
            db = get_db()
            songs = db.query(Song).filter_by(email=email).all()
            songs_list = [
                {"title": song.title, "genre": song.genre, "lyrics": song.lyrics}
                for song in songs
            ]
            return 200, songs_list
        except Exception as e:
            db.rollback()
            current_app.logger.error(e)
            return 500, {"Database error"}