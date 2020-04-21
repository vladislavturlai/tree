import json

from tree.categories.exceptions import InvalidBodyException
from tree.common.tree_structure.fields import StringField
from tree.common.tree_structure.node import Node


def parse_category_tree_request_body(body):
    """ Parses the request body, validates category tree and raise an exception if the body is invalid.
        Args:
            body: request body
        Raises:
            InvalidBodyException: If the body is invalid
    """
    try:
        categories_tree = json.loads(body)
    except json.JSONDecodeError:
        raise InvalidBodyException('Body parse error')

    return categories_tree


class CategoryNode(Node):
    fields = {
        'name': StringField()
    }
    children_field_name = 'children'
