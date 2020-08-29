import os
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
    response = post_line_notify(message="test", token=os.environ.get('LINE_NOTIFY_TOKEN_TEST'))
    assert response.status_code == 200

