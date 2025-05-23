from typing import Dict, List
from unittest.mock import patch

from fastapi.testclient import TestClient

MAX_RATING = '/disability-max-ratings'

TINNITUS = {'diagnostic_code': 6260, 'max_rating': 10}
TUBERCULOSIS = {'diagnostic_code': 7710, 'max_rating': 100}
NOT_RATED = {'diagnostic_code': 9999}


def test_max_rating_with_no_dc(client: TestClient) -> None:
    json_post_dict: Dict[str, List[int]] = {'diagnostic_codes': []}

    response = client.post(MAX_RATING, json=json_post_dict)
    assert response.status_code == 200
    response_json = response.json()

    ratings = response_json['ratings']
    assert len(ratings) == 0


def test_max_rating_with_one_dc(client: TestClient) -> None:
    json_post_dict = {'diagnostic_codes': [TINNITUS['diagnostic_code']]}

    response = client.post(MAX_RATING, json=json_post_dict)
    assert response.status_code == 200
    response_json = response.json()

    ratings = response_json['ratings']
    assert len(ratings) == 1
    assert ratings[0]['diagnostic_code'] == TINNITUS['diagnostic_code']
    assert ratings[0]['max_rating'] == TINNITUS['max_rating']


def test_max_rating_with_multiple_dc(client: TestClient) -> None:
    json_post_dict = {'diagnostic_codes': [TINNITUS['diagnostic_code'], TUBERCULOSIS['diagnostic_code']]}

    response = client.post(MAX_RATING, json=json_post_dict)
    assert response.status_code == 200
    response_json = response.json()

    ratings = response_json['ratings']
    assert len(ratings) == 2
    assert ratings[0]['diagnostic_code'] == TINNITUS['diagnostic_code']
    assert ratings[0]['max_rating'] == TINNITUS['max_rating']
    assert ratings[1]['diagnostic_code'] == TUBERCULOSIS['diagnostic_code']
    assert ratings[1]['max_rating'] == TUBERCULOSIS['max_rating']


def test_max_rating_with_duplicate_dc(client: TestClient) -> None:
    json_post_dict = {'diagnostic_codes': [TINNITUS['diagnostic_code'], TINNITUS['diagnostic_code']]}

    response = client.post(MAX_RATING, json=json_post_dict)
    assert response.status_code == 200
    response_json = response.json()
    ratings = response_json['ratings']
    assert len(ratings) == 1
    assert ratings[0]['diagnostic_code'] == TINNITUS['diagnostic_code']
    assert ratings[0]['max_rating'] == TINNITUS['max_rating']


def test_max_rating_with_too_many_dc(client: TestClient) -> None:
    json_post_dict = {'diagnostic_codes': [*range(5000, 6001)]}

    response = client.post(MAX_RATING, json=json_post_dict)
    assert response.status_code == 422


def test_max_rating_with_unmapped_dc(client: TestClient) -> None:
    json_post_dict = {'diagnostic_codes': [NOT_RATED['diagnostic_code']]}

    response = client.post(MAX_RATING, json=json_post_dict)

    assert response.status_code == 200
    response_json = response.json()

    ratings = response_json['ratings']
    assert len(ratings) == 0


def test_max_rating_with_value_below_range(client: TestClient) -> None:
    json_post_dict = {'diagnostic_codes': [4999]}

    response = client.post(MAX_RATING, json=json_post_dict)
    assert response.status_code == 400


def test_max_rating_with_value_above_range(client: TestClient) -> None:
    json_post_dict = {'diagnostic_codes': [10001]}

    response = client.post(MAX_RATING, json=json_post_dict)
    assert response.status_code == 400


def test_missing_params(client: TestClient) -> None:
    """should fail if all required params are not present"""
    json_post_dict: Dict[str, List[int]] = {}

    response = client.post(MAX_RATING, json=json_post_dict)
    assert response.status_code == 422


def test_unprocessable_content_request_does_not_have_array(client: TestClient) -> None:
    json_post_dict = {
        'diagnostic_codes': 6510,  # Should be an array
    }

    response = client.post(MAX_RATING, json=json_post_dict)
    assert response.status_code == 422


def test_unprocessable_content_request_array_has_non_int_value(client: TestClient) -> None:
    json_post_dict = {
        'diagnostic_codes': ['6510'],  # Should be an int
    }

    response = client.post(MAX_RATING, json=json_post_dict)
    assert response.status_code == 422


def test_health_check(client: TestClient) -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_health_check_with_empty_lookup_table(client: TestClient) -> None:
    with patch('src.python_src.api.MAX_RATINGS_BY_CODE', {}):
        response = client.get('/health')
        assert response.status_code == 500
        assert response.json() == {'status': 'unhealthy', 'details': 'Max Rating by Diagnostic Code Lookup table is empty.'}
