import unittest
from mockito import when, mock
from rankum.readers import DocReader
from rankum.models import Doc
from rankum.diversifiers import ScoresDiffDiversifier


class ScoresDiffDiversifierTest(unittest.TestCase):

    def test_should_diversify_rank(self):
        original_rank = [
            Doc(id="1", category=1),
            Doc(id="2", category=1),
            Doc(id="3", category=2),
            Doc(id="4", category=1),
            Doc(id="5", category=3),
            Doc(id="6", category=4)
        ]
        reader = mock(DocReader)
        when(reader).to_doc_list().thenReturn(iter(original_rank))

        diversified_rank = [
            Doc(id="1", category=1, score=2.0),
            Doc(id="3", category=2, score=1.333),
            Doc(id="5", category=3, score=1.2),
            Doc(id="6", category=4, score=1.167),
            Doc(id="2", category=1, score=1.0),
            Doc(id="4", category=1, score=0.583)
        ]
        diversifier = ScoresDiffDiversifier(reader)
        self.assertEqual(diversified_rank, list(diversifier.diversify(by='category')))

    def test_should_rank_lower_docs_with_label(self):
        original_rank = [
            Doc(id="1"),
            Doc(id="2", category=1),
            Doc(id="3", category=2),
            Doc(id="4", category=1),
            Doc(id="5", category=3),
            Doc(id="6", category=4)
        ]
        reader = mock(DocReader)
        when(reader).to_doc_list().thenReturn(iter(original_rank))

        diversified_rank = [
            Doc(id="2", category=1, score=1.5),
            Doc(id="3", category=2, score=1.333),
            Doc(id="5", category=3, score=1.2),
            Doc(id="6", category=4, score=1.167),
            Doc(id="1", score=1.0),
            Doc(id="4", category=1, score=0.75)
        ]
        diversifier = ScoresDiffDiversifier(reader)
        self.assertEqual(diversified_rank, list(diversifier.diversify(by='category')))


if __name__ == '__main__':
    unittest.main()
