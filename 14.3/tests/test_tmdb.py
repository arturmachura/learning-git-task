from unittest.mock import Mock

import tmdb_client


def test_get_poster_url_uses_default_size():
    path = "/some-poster-path.jpg"

    poster_url = tmdb_client.get_poster_url(path)

    assert poster_url == "https://image.tmdb.org/t/p/w342/some-poster-path.jpg"


def test_get_poster_url_uses_custom_size():
    path = "/some-poster-path.jpg"

    poster_url = tmdb_client.get_poster_url(path, size="original")

    assert poster_url == "https://image.tmdb.org/t/p/original/some-poster-path.jpg"


def test_get_movies_calls_correct_endpoint(monkeypatch):
    mock_call_tmdb_api = Mock()
    mock_call_tmdb_api.return_value = {"results": ["Movie 1", "Movie 2", "Movie 3"]}
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)

    tmdb_client.get_movies(how_many=8, list_type="popular")

    mock_call_tmdb_api.assert_called_once_with("movie/popular")


def test_get_movies_limits_results(monkeypatch):
    mock_call_tmdb_api = Mock()
    mock_call_tmdb_api.return_value = {"results": ["Movie 1", "Movie 2", "Movie 3"]}
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)

    movies = tmdb_client.get_movies(how_many=2, list_type="popular")

    assert movies == ["Movie 1", "Movie 2"]


def test_get_single_movie_calls_correct_endpoint(monkeypatch):
    mock_call_tmdb_api = Mock()
    mock_call_tmdb_api.return_value = {"id": 123, "title": "Some movie"}
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)

    movie = tmdb_client.get_single_movie(123)

    mock_call_tmdb_api.assert_called_once_with("movie/123")
    assert movie == {"id": 123, "title": "Some movie"}


def test_get_movie_images_calls_correct_endpoint(monkeypatch):
    mock_call_tmdb_api = Mock()
    mock_call_tmdb_api.return_value = {"backdrops": [], "posters": []}
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)

    images = tmdb_client.get_movie_images(123)

    mock_call_tmdb_api.assert_called_once_with("movie/123/images")
    assert images == {"backdrops": [], "posters": []}


def test_get_single_movie_cast_calls_correct_endpoint(monkeypatch):
    mock_call_tmdb_api = Mock()
    mock_cast = [{"name": "Actor 1"}, {"name": "Actor 2"}]
    mock_call_tmdb_api.return_value = {"cast": mock_cast, "crew": []}
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call_tmdb_api)

    cast = tmdb_client.get_single_movie_cast(123)

    mock_call_tmdb_api.assert_called_once_with("movie/123/credits")
    assert cast == mock_cast


def test_call_tmdb_api_uses_requests_get(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {"results": []}
    mock_get = Mock(return_value=mock_response)
    monkeypatch.setattr("tmdb_client.requests.get", mock_get)

    result = tmdb_client.call_tmdb_api("movie/popular")

    called_url = mock_get.call_args.args[0]
    assert called_url == "https://api.themoviedb.org/3/movie/popular"
    assert result == {"results": []}
    mock_response.raise_for_status.assert_called_once()


def test_call_tmdb_api_raises_for_bad_status(monkeypatch):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("HTTP error")
    mock_get = Mock(return_value=mock_response)
    monkeypatch.setattr("tmdb_client.requests.get", mock_get)

    try:
        tmdb_client.call_tmdb_api("movie/unknown")
        assert False, "Expected an exception to be raised"
    except Exception as exc:
        assert str(exc) == "HTTP error"
