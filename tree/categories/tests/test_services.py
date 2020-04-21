import pytest

from tree.categories.exceptions import InappropriateDataException
from tree.categories.models import Category
from tree.categories.services import CategoryData, CategoryService
from tree.categories.utils import CategoryNode


@pytest.mark.django_db
def test_category_data_save_category():
    category = CategoryData().save_category(name='name', parent_id=None)

    assert Category.objects.get(name='name').id == category


@pytest.mark.django_db
def test_category_data_save_category_raises_exception_if_category_with_given_name_already_exists(category):
    with pytest.raises(InappropriateDataException):
        CategoryData().save_category(name=category.name, parent_id=None)


@pytest.mark.django_db
def test_category_data_get_siblings(category, create_category):
    """
    Test that `get_siblings` retrieves all categories with the same parent as the given category
    without the category itself.
    """
    siblings_ids = []

    for i in range(3):
        sibling = create_category(name=f'Catogory 1.{i}', parent=category.parent)
        siblings_ids.append(sibling.id)

    result = CategoryData().get_siblings(category)
    result_ids = set(map(lambda x: x.id, result))

    for sibling_id in siblings_ids:
        assert sibling_id in result_ids


@pytest.mark.django_db
def test_category_data_get_siblings_should_return_empty_iterable_for_root_category(root_category):
    result = CategoryData().get_siblings(root_category)

    assert list(result) == []


@pytest.mark.django_db
def test_category_data_get_parents(category, create_category):
    """
    Test that `get_parents` returns all immediate parent, its parent and so on.
    """
    new_category = create_category(name='Category 1.1', parent=category)
    parents_ids = [category.id, category.parent.id]

    result = CategoryData().get_parents(new_category)
    result_ids = set(map(lambda x: x.id, result))

    for parent_id in parents_ids:
        assert parent_id in result_ids


def test_category_service_save_node_saves_node_itself(mocker):
    data_mock = mocker.MagicMock()
    name = "Category 1"
    node_data = {
        "name": name,
    }
    node = CategoryNode(node_data)

    CategoryService(data_mock).save_node(node, None)

    data_mock.save_category.assert_called_with(name, None)


def test_category_service_save_node_saves_children_for_the_given_node(mocker):
    data_mock = mocker.MagicMock()
    name = "Category 1"
    child = {"name": name}
    node_data = {
        "name": "Category 1",
        "children": [child]
    }
    node = CategoryNode(node_data)

    CategoryService(data_mock).save_node(node, None)

    data_mock.save_category.assert_called_with(child.get('name'),
                                               data_mock.save_category.return_value)


def test_category_service_save_category_tree(mocker):
    transaction_mock = mocker.patch('tree.categories.services.transaction')  # noqa
    save_node_mock = mocker.patch('tree.categories.services.CategoryService.save_node')
    category_node_mock = mocker.patch('tree.categories.services.CategoryNode')
    tree = {"name": "Category 1"}

    data_mock = mocker.MagicMock()

    res = CategoryService(data_mock).save_category_tree(tree)

    save_node_mock.assert_called_with(category_node_mock.return_value, None)
    assert res == save_node_mock.return_value
