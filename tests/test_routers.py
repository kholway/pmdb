from app.models.movie import Movie

"""Tests the API routes"""


def test_route_create_movie(client, movie_data):
    response = client.post("/movies/", json=movie_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == movie_data["title"]
    assert response_data["year"] == movie_data["year"]
    assert response_data["director"] == movie_data["director"]
    assert response_data["runtime"] == movie_data["runtime"]
    assert response_data["country"] == movie_data["country"]
    assert "id" in response_data

    # Not implemented
    # assert response_data["mpaa_rating"] == movie_data["mpaa_rating"]   


def test_route_create_movie_invalid(client):
    response = client.post("/movies/", json={
        "title": "Monty Python and the Holy Grail",
        "year": 1
    })
    
    assert response.status_code == 422
    data = response.json()
    assert "title" not in data
    assert "year" not in data
    assert "id" not in data


def test_route_read_movie_exists(client, movie_data):
    # Populate the database
    db = client.db_session
    mov = Movie(**movie_data)
    db.add(mov)
    db.commit()
    movie_id = mov.id

    # Try to read a movie
    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == movie_data["title"]
    assert response_data["year"] == movie_data["year"]
    assert response_data["director"] == movie_data["director"]
    assert response_data["runtime"] == movie_data["runtime"]
    assert response_data["country"] == movie_data["country"]
    assert "id" in response_data


def test_route_read_movie_does_not_exist(client):
    # Try to read a movie that's not there
    response = client.get(f"/movies/100")
    assert response.status_code == 404
    response_data = response.json()
    assert "detail" in response_data