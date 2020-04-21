class InvalidBodyException(Exception):
    pass


class InvalidFieldException(Exception):
    pass


class InappropriateDataException(Exception):
    pass


class CategoryServiceException(Exception):
    def __init__(self, data):
        self.data = data
