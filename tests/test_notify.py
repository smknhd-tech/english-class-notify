from notify.notify import post_line_notify
from unittest import mock
import pytest
import requests
from typing import NamedTuple


def test_post_line_notify_no_exist_img_path():
    with pytest.raises(FileNotFoundError):
        post_line_notify(message="test", token="test", img_path="存在しないパス")


def test_post_line_notify_invalid_token():
    response = post_line_notify(message="test", token="invalid_token")
    assert response.status_code == 401


def test_post_line_notify_valid_token():
    class Response(NamedTuple):
        status_code: int

    requests.post = mock.Mock(return_value=Response(200))
    response = post_line_notify(message="test", token="valid_token")
    assert response.status_code == 200
