from src.triples_from_openie import TriplesFromOpenieGenerator
from src.triples_from_dependencies import TriplesFromDependenciesGenerator


class TriplesPicker:
    openie_generator = TriplesFromOpenieGenerator()
    dep_generator = TriplesFromDependenciesGenerator()

    def _get_best_openie_triples(self, sentence_metadata):
        return self.openie_generator.get_triples(sentence_metadata)

    def _get_dep_triple(self, sentence_metadata):
        return self.dep_generator.get_triple(sentence_metadata)

    def get_triples(self, sentence_metadata):
        triples = []
        openie_triples = []
        dep_triples = []
        if sentence_metadata['triples']:
            openie_triples = self._get_best_openie_triples(sentence_metadata)
        #else:
        #dep_triples = self._get_dep_triple(sentence_metadata)

        if openie_triples:
            triples += openie_triples
        if dep_triples:
            triples += dep_triples

        return triples
