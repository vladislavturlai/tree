import pytest


@pytest.fixture
def api_rf():
    """
    A Django Rest Framework `APIRequestFactory` instance.
    """
    from rest_framework.test import APIRequestFactory
    return APIRequestFactory()


# Categories fixtures
@pytest.fixture
def create_category():
    """
    A function to create `categories.Category` instances.
    """
    from tree.categories.models import Category

    def _create_category(name, parent=None, **kwargs):
        return Category.objects.create(
            name=name,
            parent=parent,
            **kwargs
        )
    return _create_category


@pytest.fixture
def root_category(create_category):
    """
    A default `categories.Category` instance without a parent category.
    """
    return create_category(
        name='Root category'
    )


@pytest.fixture
def category(root_category, create_category):
    """
    A default `categories.Category` instance.
    """
    return create_category(
        name='Subcategory', parent=root_category
    )
