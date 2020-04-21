import json

import pytest
from rest_framework.reverse import reverse

from tree.categories.views import CategoriesView


@pytest.fixture
def valid_post_body():
    return json.dumps({
        "name": "Category 1",
        "children": [
            {
                "name": "Category 1.1",
                "children": [
                    {
                        "name": "Category 1.1.1",
                        "children": [
                            {
                                "name": "Category 1.1.1.1"
                            }
                        ]
                    }
                ]
            }
        ]
    })


@pytest.fixture
def invalid_post_body():
    return json.dumps({
        "name": "Category 1",
        "children": [
            {
                "name": "Category 1.1",
                "children": [
                    {
                        "name": "Category 1.1",  # duplicate name
                        "children": [
                            {
                                "name": "Category 1.1.1.1"
                            }
                        ]
                    }
                ]
            }
        ]
    })


@pytest.mark.django_db
def test_categories_view_returns_201_for_correct_request(api_rf, valid_post_body):
    view = CategoriesView.as_view()
    request = api_rf.post(reverse('categories:categories'), valid_post_body, content_type='application/json')
    response = view(request)
    assert response.status_code == 201


@pytest.mark.django_db
def test_categories_view_returns_400_for_incorrect_request(api_rf, invalid_post_body):
    view = CategoriesView.as_view()
    request = api_rf.post(reverse('categories:categories'), invalid_post_body, content_type='application/json')
    response = view(request)
    assert response.status_code == 400
