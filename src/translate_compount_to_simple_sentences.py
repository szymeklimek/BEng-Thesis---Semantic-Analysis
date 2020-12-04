from nltk.parse import CoreNLPParser
from nltk.parse import CoreNLPDependencyParser
import json
from src.triples_from_dependencies import TriplesFromDependenciesGenerator
from src.triples_from_openie import TriplesFromOpenieGenerator


# parser = CoreNLPParser(url='http://localhost:9000')
# parser = CoreNLPDependencyParser(url='http://localhost:9000')
#
# print(list(parser.parse('What is the airspeed of an unladen swallow ?'.split())))
#
# parse, = parser2.raw_parse('Marek\'s disease vaccines use a non-disease-causing virus to infect cells')
# parse1, = parser.parse('Sachin Tendulkar, who is a MP of Indian Parliament, played cricket')
# print(parse.tree())
# print(parse.to_conll(4))

def contains_verbs(tokens):
    for token in tokens:
        if str(token['pos']).startswith('V'):
            return True
    return False

with open(
        '/Users/aprzybycien/projects/inzynierka/BEng-Thesis---Semantic-Analysis/data/vaccine-articles/triples/TRIPLESMETAarticle13.json',
        encoding='ISO-8859-1') as json_file:
    print(json_file)
    sentences = json.load(json_file)
    triples_from_dep = TriplesFromDependenciesGenerator()
    triples_from_openie = TriplesFromOpenieGenerator()
    for sentence in sentences:
        if not contains_verbs(sentence['tokens']):
            continue
        print(sentence['sentence'])
        print('\n')
        openie_triple = triples_from_openie.get_triple(sentence)
        if openie_triple:
            print("Openie triple: ", openie_triple)
        dep_triple = triples_from_dep.get_triple(sentence)
        print("dep triple: ", dep_triple)
        print('\n')
        print('\n')

