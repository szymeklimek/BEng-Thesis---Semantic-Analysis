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


# def choose_correct_triple(sentence):
#     # todo: get supporting words based on dependencies
#     if sentence['triples']:
#         return sentence['triples']
#     else:
#         print("Openie could not find a triple ;(")
#         return {}
#
#
# def get_triple_from_openie(sentence):
#     return choose_correct_triple(sentence)
#
#
# def get_subj_indexes(sentence):
#     sub_indexes = []
#     for idx, dep in enumerate(sentence['dependencies']):
#         if 'nsubj' in str(dep['dep']):
#             sub_indexes.append(idx)
#     return sub_indexes
#
#
# def check_if_simple_sentence(sub_count):
#     if len(sub_count) == 1:
#         return True
#     return False
#
#
# def get_triple_from_simple_sentence(sentence):
#     sub = ""
#     rel = ""
#     obj = ""
#     sub_addons = {}
#     rel_addons = {}
#     obj_addons = {}
#     is_cop = False
#     cop = ""
#     for dep in sentence['dependencies']:
#
#         if dep['dep'] == 'nsubj':
#             pos = get_pos_of_word(sentence, dep['governorGloss'])
#             if not str(pos).startswith('V'):
#                 obj = dep['governorGloss']
#                 sub = dep['dependentGloss']
#                 is_cop = True
#             else:
#                 rel = dep['governorGloss']  # ?
#                 sub = dep['dependentGloss']
#             continue
#         if dep['dep'] == 'nsubj:pass':
#             sub = dep['dependentGloss']
#             continue
#         if dep['dep'] == 'aux:pass':
#             rel = str(dep['dependentGloss']) + " " + str(dep['governorGloss'])
#         if dep['dep'] == 'nmod':
#             if obj:
#                 obj = obj + " " + dep['dependentGloss']
#             else:
#                 obj = dep['dependentGloss']
#             continue
#         if dep['dep'] == 'cop':
#             cop = dep['dependentGloss']
#             continue
#         if dep['dep'] == 'obl':
#             obj = dep['dependentGloss'] + " " + obj
#             continue
#         if 'obj' in str(dep['dep']):
#             obj = dep['governorGloss']
#             continue
#         # normally in nsubj governor = verb (rel), dependent = subject and obj is object, if governor is not a verb
#         # then governor = object, dependent = subject and cop is the rel
#     if is_cop:
#         rel = cop
#     return {'sub': sub, 'rel': rel, 'obj': obj}
#
# def check_if_found(found, idx_gov, idx_dep):
#     if idx_gov in found or idx_dep in found:
#         return True
#     return False
#
# def reccurent_find_all(deps_to_consider, found=[], to_find=[]):
#     deps = []
#     temp_deps_to_consider = deps_to_consider[:]
#     for idx, dep in enumerate(temp_deps_to_consider):
#         if dep['governor'] in to_find or dep['dependent'] in to_find:
#             if not check_if_found(found, dep['governor'], dep['dependent']):
#                 deps.append(dep)
#                 new_deps_to_consider = temp_deps_to_consider[:]
#                 new_deps_to_consider.pop(idx)
#                 to_find_idx = 0
#                 if dep['governor'] in to_find:
#                     to_find_idx = dep['dependent']
#                 else:
#                     to_find_idx = dep['governor']
#                 more_deps = reccurent_find_all(new_deps_to_consider, to_find, [to_find_idx])
#                 if more_deps:
#                     deps = deps + more_deps
#     return deps
#
#
# def find_connected_deps(sub, deps_to_consider):
#     gov_id = sub['governor']
#     dep_id = sub['dependent']
#     deps = []
#     idx_sub = 0
#     temp_deps_to_consider = deps_to_consider[:]
#     for idx, dep in enumerate(deps_to_consider):
#         if dep['governor'] == sub['governor'] and dep['dependent'] == sub['dependent']:
#             idx_sub = idx
#     temp_deps_to_consider.pop(idx_sub)
#     deps = reccurent_find_all(temp_deps_to_consider, to_find=[gov_id, dep_id])
#     deps.append(sub)
#     return deps
#
#
# def get_dependencies_tree_from_compound(sentence, sub_indexes):
#     deps_to_consider = []
#     for dep in sentence['dependencies']:
#         if str(dep['dep']) not in ['mark', 'acl', 'appos', 'advcl', 'cc', 'ccomp', 'conj', 'dep', 'parataxis', 'ref', 'punct']:
#             deps_to_consider.append(dep)
#     # build deps trees for nsubjs
#     dependencies = []
#     for sub_idx in sub_indexes:
#         sub = sentence['dependencies'][sub_idx]
#         dependencies.append(find_connected_deps(sub, deps_to_consider))
#     return dependencies
#
#
# def get_triple_from_dep(sentence):
#     # parse, = parser.raw_parse(sentence['sentence'])
#     # print(parse.tree())
#     # print(parse.to_conll(4))
#     triples = []
#     sub_indexes = get_subj_indexes(sentence)
#     is_simple = check_if_simple_sentence(sub_indexes)
#     if is_simple:
#         triples.append(get_triple_from_simple_sentence(sentence))
#     else:
#         triples = []
#         simple_sentence_deps = get_dependencies_tree_from_compound(sentence, sub_indexes)
#         for deps in simple_sentence_deps:
#             triples.append(get_triple_from_simple_sentence({'dependencies': deps, 'tokens': sentence['tokens'], 'sentence': sentence['sentence']}))
#     return triples
#
#
# def get_pos_of_word(sentence, word):
#     for token in sentence['tokens']:
#         if token['word'] == word:
#             return token['pos']
#
#
# def get_index_of_word(sentence, word):
#     for token in sentence['tokens']:
#         if token['word'] == word:
#             return token['index']


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

