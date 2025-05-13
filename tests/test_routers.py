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


def test_route_read_movie_exists(client):    
    pass


def test_route_read_movie_does_not_exist(client):
    pass


def test_route_read_movie_invalid_id(client):
    pass