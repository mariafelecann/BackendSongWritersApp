
def test_add_song_route(client):

    response = client.post("/crud/add", json={
        "title": "Test Song",
        "email": "test@example.com",
        "lyrics": "La la la",
        "genre": "Pop"
    })
    assert response.status_code == 200
    assert response.json["message"] == "Song added successfully"

    response = client.post("/crud/add", json={
        "title": "Test Song",
        "email": "test@example.com",
        "lyrics": "La la la",
        "genre": "Pop"
    })
    assert response.status_code == 409
    assert "error" in response.json

    response = client.post("/crud/add", json={
        "title": "",
        "email": "test@example.com",
        "lyrics": "Lyrics",
        "genre": "Pop"
    })
    assert response.status_code == 400

def test_get_songs_route(client):

    client.post("/crud/add", json={
        "title": "Another Song",
        "email": "user@example.com",
        "lyrics": "Lyrics here",
        "genre": "Jazz"
    })

    response = client.get("/crud/songs?email=user@example.com")
    assert response.status_code == 200
    songs = response.json
    assert isinstance(songs, list)
    assert any(song["title"] == "Another Song" for song in songs)

    response = client.get("/crud/songs")
    assert response.status_code == 400

def test_delete_song_route(client):
    client.post("/crud/add", json={
        "title": "Delete Me",
        "email": "delete@example.com",
        "lyrics": "Lyrics",
        "genre": "Pop"
    })

    response = client.post("/crud/delete", json={
        "title": "Delete Me",
        "email": "delete@example.com"
    })
    assert response.status_code == 200

    response = client.post("/crud/delete", json={
        "title": "Delete Me",
        "email": "delete@example.com"
    })
    assert response.status_code == 404

    response = client.post("/crud/delete", json={
        "title": "",
        "email": ""
    })
    assert response.status_code == 400
