class MissingDocIdException(Exception):
    """Raise when document id is missing"""

    def __init__(self, message: str):
        super().__init__(message)


class EmptyDocListException(Exception):
    """Raise when document list is empty"""

    def __init__(self, message: str):
        super().__init__(message)
