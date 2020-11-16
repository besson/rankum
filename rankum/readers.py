from typing import List, Iterator
from rankum.models import Doc
from rankum.exceptions import MissingDocIdException, EmptyDocListException, \
    MissingDocReaderInfoException, FetchDocListException

import json
import requests

class DocReader:
    """ Reader document list from different sources"""

    def to_doc_list(self) -> Iterator[Doc]:
        """
        Convert document list to Iterator[Doc]
        :return doc iterator (Iterator[Doc]): iterator for converted document list
        """
        raise NotImplemented()


class JsonDocReader(DocReader):
    """ Reader document list from a JSON string """

    def __init__(self, json_str: str):
        self.json_str = json_str

    def to_doc_list(self) -> Iterator[Doc]:
        """
        Convert document list to Iterator[Doc]
        :return doc iterator (Iterator[Doc]): iterator for converted document list
        """
        doc_dict = self._json_to_dict()

        if len(doc_dict) == 0:
            raise EmptyDocListException(message='Document list is empty')

        def iterator_over(all_docs: List):
            for _doc in all_docs:
                if 'id' not in _doc:
                    raise MissingDocIdException(message='Field "id" is mandatory for each document')

                yield Doc(id=str(_doc.pop('id')), **_doc)

        return iterator_over(doc_dict)

    def _json_to_dict(self) -> dict:
        """
        Convert json string to Dictionary
        :return:
        """
        try:
            doc_dict = json.loads(self.json_str)
        except TypeError as e:
            raise EmptyDocListException(message='Document list is invalid')

        return doc_dict


class SolrDocReader(DocReader):
    """ Reader document list from a Solr query """
    def __init__(self, host: str, query: str):
        if host is None:
            raise MissingDocReaderInfoException(message='Host name is missing')

        if query is None:
            raise MissingDocReaderInfoException(message='Query name is missing')

        self.host = host
        self.query = query

    def to_doc_list(self) -> Iterator[Doc]:
        """
        Convert Solr query results into Iterator[Doc]
        :return doc iterator (Iterator[Doc]): iterator for converted document list
        """
        response = requests.get(f'{self.host}/{self.query}')

        if response.status_code is not 200:
            raise FetchDocListException(message=f'Failed to fetch document from {response.json()}')

        def fetch_docs():
            docs = response.json().get('response', []).get('docs', [])
            for _doc in docs:
                if 'id' not in _doc:
                    raise MissingDocIdException(message='Field "id" is mandatory for each document')

                yield Doc(id=str(_doc.pop('id')), **_doc)

        return fetch_docs()