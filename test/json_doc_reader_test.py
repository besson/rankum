import unittest
from rankum.models import Doc
from rankum.exceptions import MissingDocIdException, EmptyDocListException
from rankum import JsonDocReader


class JsonDocReaderTest(unittest.TestCase):

    def test_should_json_list(self):
        input_json = '[{"id": 1, "category": 1}, {"id": "2", "category": 2}]'
        expect = [Doc(id="1", category=1), Doc(id="2", category=2)]

        actual = list(JsonDocReader(input_json).to_doc_list())
        self.assertEqual(expect, actual)

    def test_raise_an_exception_when_id_is_missing(self):
        input_json = '[{"id": 1, "category": 1}, {"category": 2}]'
        with self.assertRaises(MissingDocIdException):
            list(JsonDocReader(input_json).to_doc_list())

    def test_raise_an_exception_when_doc_list_is_empty(self):
        input_json = '[]'
        with self.assertRaises(EmptyDocListException):
            list(JsonDocReader(input_json).to_doc_list())

    def test_raise_an_exception_when_doc_list_is_none(self):
        input_json = None
        with self.assertRaises(EmptyDocListException):
            list(JsonDocReader(input_json).to_doc_list())


if __name__ == '__main__':
    unittest.main()
