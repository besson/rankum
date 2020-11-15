from typing import List
from collections import defaultdict
from rankum.models import Doc
from rankum.readers import DocReader


class RankDiversifier():
    """ Diversifying rank strategies"""

    def __init__(self, reader: DocReader):
        self.reader = reader

    def diversify(self, by: str) -> List[Doc]:
        """
        Diversifying document list based on a target
        :param by (str): criteria (target) to diversify by. It is an attribute common to all documents
        :return diversified rank (List[Doc]): original document list re-ranked by diversified target
       """
        raise NotImplemented


class ScoresDiffDiversifier(RankDiversifier):
    """
    This algorithm calculates the final document score based on its global relevance (original rank position) and
    local relevance (rank position in the group we are diversifying by).
    This algorithm is proposed in this paper:
    https://www.researchgate.net/publication/266658487_Using_score_differences_for_search_result_diversification
    """

    def __init__(self, reader: DocReader):
        super().__init__(reader)
        self.iter_docs = reader.to_doc_list()

    def diversify(self, by: str) -> List[Doc]:
        """
        Diversifying document list using Scores diff strategy
        :param by (str): criteria (target) to diversify by. It is an attribute common to all documents
        :return diversified rank (List[Doc]): original document list re-ranked by diversified target
        """
        local_rank = defaultdict(int)
        global_rank = []

        for i, _doc in enumerate(self.iter_docs):
            target = _doc.get(by)
            local_score = 0 if target is None else 1.0 / (local_rank.get(target, 0) + 1)
            global_score = 1.0 / (i + 1)
            _doc.score = round(local_score + global_score, 3)

            local_rank[target] += 1
            global_rank.append(_doc)

        return sorted(global_rank, reverse=True)
