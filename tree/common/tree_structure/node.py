from collections import defaultdict

from tree.common.tree_structure.exceptions import NodeValidationException, FieldException
from tree.common.tree_structure.fields import ListField, StringField
from tree.common.tree_structure.utils import empty


class Node:
    """
    Usage:
        try:
            node = Node({...})
            node.validate
        except NodeValidationException as e:
            ...
    """
    fields = {}
    children_field_name = 'children'

    def __init__(self, tree):
        self._tree = tree
        self._inner_tree = {}

        self._errors = defaultdict(list)

        # add a default ListField for children
        self._fields = {
            self.children_field_name: ListField(required=False, null=False)
        }
        # collect fields throughout the inheritance chain
        for cls in reversed(self.__class__.__mro__):
            self._fields.update(getattr(cls, "fields", {}))

    def validate(self):
        self._build_inner_tree()

        self._validate_fields()
        if self.children_field_name not in self._errors:
            self._validate_children()

        if self._errors:
            raise NodeValidationException(self._errors)

    def _build_inner_tree(self):
        for field_name, _ in self._fields.items():
            self._inner_tree[field_name] = self._tree.get(field_name, empty)

    def _validate_fields(self):
        for field_name, field_class in self._fields.items():
            try:
                field_class.validate(self._inner_tree[field_name])
            except FieldException as e:
                self._errors[field_name].extend(e.errors)

    def _validate_children(self):
        for i, child in enumerate(self.children):
            try:
                child.validate()
            except NodeValidationException as e:
                self._errors[self.children_field_name].append({i: e.errors})

    def get_field_value(self, field_name):
        if field_name in self._fields:
            return self._tree.get(field_name)
        else:
            raise KeyError(field_name)

    @property
    def children(self):
        children = self._tree.get(self.children_field_name, [])
        return [self.__class__(child_node) for child_node in children]


class CategoryNode(Node):
    fields = {
        'name': StringField()
    }
    children_field_name = 'children'
