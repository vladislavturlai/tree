from tree.common.tree_structure.exceptions import FieldException
from tree.common.tree_structure.utils import empty
from tree.common.tree_structure.validators import is_string, is_list


class Field:
    validators = None

    def __init__(self,
                 required=True,
                 null=False):
        self.required = required
        self.null = null

        # collect validators throughout the inheritance chain
        self._validators = []
        for cls in reversed(self.__class__.__mro__):
            validators = getattr(cls, "validators", None)
            if validators:
                self._validators.extend(validators)

    def validate(self, value):
        self._validate_empty(value)
        if value is None or value is empty:
            return

        self._run_validators(value)

    def _run_validators(self, value):
        errors = []
        for validator, error_message in self._validators:
            result = validator(value)
            if not result:
                errors.append(error_message)

        if errors:
            raise FieldException(errors)

    def _validate_empty(self, value):
        if self.required and value is empty:
            raise FieldException(['This field is required'])
        if not self.null and value is None:
            raise FieldException(['This field cannot be null'])


class StringField(Field):
    validators = [(is_string, 'This field must be a string')]


class ListField(Field):
    validators = [(is_list, 'This field must be a list')]
