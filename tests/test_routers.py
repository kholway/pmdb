"""Tests the API routes"""


def test_route_create_movie(client):
    response = client.post("/movies/", json={
        "title": "Monty Python and the Holy Grail",
        "director": "Terry Gilliam, Terry Jones",
        "runtime": 91,
    })

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Monty Python and the Holy Grail"
    assert data["director"] == "Terry Gilliam, Terry Jones"
    assert data["runtime"] == 91
    assert "id" in data


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