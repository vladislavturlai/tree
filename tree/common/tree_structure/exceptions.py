class FieldException(Exception):
    def __init__(self, errors):
        self.errors = errors


class NodeValidationException(Exception):
    def __init__(self, errors):
        self.errors = errors
