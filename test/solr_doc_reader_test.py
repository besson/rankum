import unittest
import requests
import json
from mockito import when, verify, unstub, mock
from rankum.exceptions import MissingDocReaderInfoException, FetchDocListException
from rankum import SolrDocReader
from rankum.models import Doc


class SolrDocReaderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.host = 'http://my_host.com:8983'
        self.query = 'select?q=rock+music'

    def tearDown(self) -> None:
        unstub()

    def test_should_raise_exception_when_host_is_none(self):
        with self.assertRaises(MissingDocReaderInfoException):
            SolrDocReader(host=None, query=self.query)

    def test_should_raise_exception_when_query_is_none(self):
        with self.assertRaises(MissingDocReaderInfoException):
            SolrDocReader(host=self.host, query=None)

    def test_should_send_http_request(self):
        response = mock({'status_code': 200, 'text': 'Ok'})
        when(requests).get(...).thenReturn(response)
        reader = SolrDocReader(host=self.host, query=self.query)

        reader.to_doc_list()
        verify(requests).get(f'{self.host}/{self.query}')

    def test_raise_exception_when_response_is_not_200(self):
        response = mock({'status_code': 500, 'text': 'Server Error'})
        when(requests).get(...).thenReturn(response)
        reader = SolrDocReader(host=self.host, query=self.query)

        with self.assertRaises(FetchDocListException):
            reader.to_doc_list()

    def test_convert_response_to_document_list(self):
        response = mock({'status_code': 200, 'text': 'Ok'})
        solr_response = _read_solr_response()
        when(response).json().thenReturn(solr_response)
        when(requests).get(...).thenReturn(response)

        expected = [
            Doc(id='1', category='cellphones', _version_=1674206250103996416),
            Doc(id='2', category='cellphones', _version_=1674206250224582656),
            Doc(id='3', category='accessories', _version_=1674206250229825536),
            Doc(id='4', category='cellphones', _version_=1674206250235068416),
            Doc(id='5', category='services', _version_=1674206250238214144),
            Doc(id='6', category='electronics', _version_=1674206250242408448)
        ]
        reader = SolrDocReader(host=self.host, query=self.query)
        self.assertEqual(expected, list(reader.to_doc_list()))

    def test_convert_to_empty_list_when_response_is_empty(self):
        response = mock({'status_code': 200, 'text': 'Ok'})
        solr_response = _read_solr_response(file='fixtures/empty_solr_payload.json')
        when(response).json().thenReturn(solr_response)
        when(requests).get(...).thenReturn(response)

        reader = SolrDocReader(host=self.host, query=self.query)
        self.assertEqual([], list(reader.to_doc_list()))


def _read_solr_response(file='fixtures/solr_payload.json'):
    with open(file) as json_file:
        data = json.load(json_file)

    return data


if __name__ == '__main__':
    unittest.main()
