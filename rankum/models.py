from functools import total_ordering


@total_ordering
class Doc:
    """Represents a document to be re-ranked"""

    def __init__(self, id: str, **kwargs):
        self.id = id
        self.__dict__.update(kwargs)

    def set_score(self, score: float):
        """
        Set a document score
        :param score (float): document score
        :return None
        """
        self.score = score

    def get(self, key: str):
        """
        Get a document field
        :param key (str): document field name
        :return document field value
        """
        return self.__dict__.get(key)

    def __eq__(self, other):
        return self.id == other.id and self.__dict__ == other.__dict__

    def __lt__(self, other):
        return self.__dict__.get('score', 0) < other.__dict__.get('score', 0)

    def __repr__(self):
        return f'Doc(id={self.id}, {self.__dict__})'
