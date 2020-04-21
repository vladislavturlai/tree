import json

import pytest

from tree.categories.exceptions import InvalidBodyException
from tree.categories.utils import parse_category_tree_request_body


def test_parse_category_tree_request_body(mocker):
    json_loads_mock = mocker.patch('tree.categories.utils.json.loads',)
    body = {}

    res = parse_category_tree_request_body(body)

    assert res == json_loads_mock.return_value


def test_parse_category_tree_request_body_raise_exc_when_unable_to_parse_body(mocker):
    json_loads_mock = mocker.patch('tree.categories.utils.json.loads',  # noqa
                                   side_effect=json.JSONDecodeError('msg', 'doc', 1))
    body = {}

    with pytest.raises(InvalidBodyException):
        parse_category_tree_request_body(body)
