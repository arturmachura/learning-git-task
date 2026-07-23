import pytest
from unittest.mock import Mock

from main import app
import tmdb_client


@pytest.mark.parametrize('list_type', tmdb_client.MOVIE_LISTS)
def test_homepage(monkeypatch, list_type):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get('/', query_string={'list_type': list_type})
        assert response.status_code == 200
        api_mock.assert_called_once_with(f'movie/{list_type}')


def test_homepage_falls_back_to_popular_for_unknown_list_type(monkeypatch):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get('/', query_string={'list_type': 'not-a-real-list'})
        assert response.status_code == 200
        api_mock.assert_called_once_with('movie/popular')
