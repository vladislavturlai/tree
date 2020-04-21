from django.db import transaction

from tree.categories.exceptions import InappropriateDataException, CategoryServiceException
from tree.categories.models import Category
from tree.categories.utils import CategoryNode

from tree.common.tree_structure.exceptions import NodeValidationException


class CategoryData:
    def save_category(self, name, parent_id):
        """ Saves a category to DB using the given params.
            Makes sure that a category with the same name doesn't exist.

        Args:
            name(str): category name
            parent_id(int, None): id of its parent element, Can be None if it's a root tree_structure.
        Raises:
            InappropriateDataException: if a category with the same name already exists
        """
        node_obj, created = Category.objects.get_or_create(name=name,
                                                           defaults={'parent_id': parent_id})
        if not created:  # name isn't unique
            raise InappropriateDataException(f"Category named '{name}' already exists")

        return node_obj.id

    def get_siblings(self, category):
        """ Retrieves siblings (categories that have the same immediate parent) for the given category.
            Does not include the category itself.
        Args:
            category(models.Category): category to retrieve 'siblings' from.
        Returns:
            Iterable(models.Category): siblings
        """
        parent = category.parent
        if category.parent is not None:
            return Category.objects.filter(parent=parent).exclude(id=category.id)
        return Category.objects.none()

    def get_parents(self, category):
        """ Retrieves all parents (immediate parent, its parent and so on) for the given category.

        Args:
            category(models.Category): category to retrieve 'parents' from.
        Returns:
            Iterable(models.Category): all parents
        """
        parents = []
        parent = category.parent

        # can be replaced by a recursive SQL query, but that will make the code less readable.
        while parent is not None:
            parents.append(parent)
            parent = parent.parent
        return parents


class CategoryService:
    def __init__(self, data):
        self._data = data

    def save_node(self, node, parent_id):
        """ Recursively saves tree_structure
        Args:
            node(CategoryNode): category tree (or a subtree)
            parent_id(int, None): id of the parent element for the given tree_structure. Can be None if it's a root tree_structure.
        Returns:
            int: id of a saved tree_structure
        """
        name = node.get_field_value('name')
        node_id = self._data.save_category(name, parent_id)

        for child in node.children:
            self.save_node(child, node_id)
        return node_id

    def save_category_tree(self, tree):
        """ Validates the tree
            Saves the tree to DB.
            This is an atomic change.

        Args:
            tree(dict): Category tree
                E.g.:
                {
                    "name":"Category 1",
                    "children":[{...}, {...}]
                }
        Returns:
            int: Id of the root element
        Raises:
            CategoryServiceException: if the tree has invalid data.
        """

        try:
            root_node = CategoryNode(tree)
            root_node.validate()
        except NodeValidationException as e:
            raise CategoryServiceException(data=e.errors)

        try:
            with transaction.atomic():
                root_id = self.save_node(root_node, None)
                return root_id
        except InappropriateDataException as e:
            raise CategoryServiceException(data={'error': str(e)})
