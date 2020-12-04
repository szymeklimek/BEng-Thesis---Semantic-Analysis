from itertools import product
from collections import defaultdict

class TriplesFromOpenieGenerator:

    def _choose_correct_triples(self, sentence):
        if not sentence['triples']:
            print("Openie could not find a triple ;(")
            return []
        # todo: get supporting words based on dependencies
        sub = ""
        rel = ""
        obj = ""
        for triple in sentence['triples']:
            if self._check_if_sub_correct(triple['subject'], sentence):
                sub = self._find_longer_string(sub, triple['subject'])
            rel = self._find_longer_string(rel, triple['relation'])
            if self._check_if_obj_is_nounish(triple['object'], sentence):
                obj = self._find_longer_string(obj, triple['object'])

        new_sub = self._get_compounds_from_words(sub.split(" "), sentence)
        new_rel = self._get_compounds_from_words(rel.split(" "), sentence)
        new_obj = self._get_compounds_from_words(obj.split(" "), sentence)

        subs, sub_support = self._get_supporting_words(new_sub, sentence, fallbacks=["RB", "PRP"])
        rels, rel_support = self._get_supporting_words(new_rel, sentence, type="V")
        objs, obj_support = self._get_supporting_words(new_obj, sentence, fallbacks=["JJ"])


        triples = self._get_all_triples(subs, rels, objs, sub_support, rel_support, obj_support)
        return triples

    def _check_if_sub_correct(self, sub, metadata):
        deps_to_consider = []
        for dep in metadata['dependencies']:
            if 'nsubj' in dep['dep']:
                deps_to_consider.append(dep)
                break
        for word in sub.split(" "):
            for dep in deps_to_consider:
                # check also dep['dependentGloss']???
                if dep['dependentGloss'] == word:
                    return True
        return False

    def _check_if_obj_is_nounish(self, obj, metadata):
        words = obj.split(" ")
        for token in metadata['tokens']:
            for word in words:
                if token['word'] == word and str(token['pos']).startswith("N"):
                    return True
                elif token['word'] != word:
                    continue
        return False



    def _find_longer_string(self, curr_string, candidate_string, type="N"):
        word_count_sub = len(str(candidate_string).split(" "))
        if word_count_sub >= len(curr_string.split(" ")):
            return candidate_string
        return curr_string

    def _get_compounds_from_words(self, words, sentence):
        words_compounds = []
        deps_to_consider = []
        for dep in sentence['dependencies']:
            if str(dep['dep']) == 'compound' or str(dep['dep']) == 'aux:pass':
                deps_to_consider.append(dep)
        new_words_list = []
        for word in words:
            if not self._check_if_already_in_compund(word, words_compounds):
                compound = self._find_compound(word, deps_to_consider)
                if compound:
                    words_compounds.append(compound)
                    new_words_list.append(" ".join(compound))
                else:
                    new_words_list.append(word)
        return new_words_list


    def _recurent_find_compound(self, deps_to_conider, to_find= "", found = []):
        com_map = {}
        for dep in deps_to_conider:
            if dep['governorGloss'] not in found and dep['dependentGloss'] not in found:
                if dep['governorGloss'] == to_find or dep['dependentGloss'] == to_find:
                    com_map[dep['governor']] = dep['governorGloss']
                    com_map[dep['dependent']] = dep['dependentGloss']
                    new_to_find = ""
                    if dep['governorGloss'] == to_find:
                        new_to_find = dep['dependentGloss']
                    else:
                        new_to_find = dep['governorGloss']
                    new_found = found[:]
                    new_found.append(to_find)
                    more_com_map = self._recurent_find_compound(deps_to_conider, to_find=new_to_find, found=new_found)

                    if more_com_map:
                        com_map.update(more_com_map)
        return com_map

    def _find_compound(self, word, deps_to_conider):
        compound = []
        com_map = self._recurent_find_compound(deps_to_conider, to_find=word)
        if com_map:
            compound = [com_map[k] for k in sorted(com_map)]
        return compound

    def _check_if_already_in_compund(self, word_to_check, words_compounds):
        for compounds in words_compounds:
            for word in compounds:
                if word == word_to_check:
                    return True
        return False

    def _get_supporting_words(self, words_clusters, sentence, type="N", fallbacks=[]):
        bare_word = []
        sub_support = {}
        for words in words_clusters:
            if len(words.split(" ")) == 1:
                word = words
                for token in sentence['tokens']:
                    if token['word'] == word:
                        if token['pos'].startswith(type):
                            bare_word.append(word)
                            continue
                        else:
                            if not token['pos'] in sub_support.keys():
                                sub_support[token['pos']] = []
                            if word not in sub_support[token['pos']]:
                                sub_support[token['pos']].append(word)
                                continue
            else:
                bare_word.append(words)
        if not bare_word and fallbacks:
            for fallback in fallbacks:
                if fallback in sub_support.keys():
                    bare_word += sub_support[fallback]
                    del sub_support[fallback]
        return bare_word, sub_support

    def _get_all_triples(self, subs, rels, objs, sub_support, rel_support, obj_support):
        if not subs or not rels or not objs:
            print("None correct triples :(")
            return []
        product_triples = product(subs, rels, objs)
        triples = []
        for ptriple in product_triples:
            triple = dict(sub=ptriple[0], rel=ptriple[1], obj=ptriple[2], sub_support=sub_support,
                          rel_support=rel_support, obj_support=obj_support)
            triples.append(triple)
        return triples

    def get_triples(self, sentence):
        return self._choose_correct_triples(sentence)
