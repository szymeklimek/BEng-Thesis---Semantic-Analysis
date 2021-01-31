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
        compounds_ids = self._get_compounds_from_words(sentence)
        chosen_triples = []
        for triple in sentence['triples']:
            if self._check_if_sub_correct(triple['subject'], sentence):
                sub = triple['subject']
            if self._check_if_relation_is_verbish(triple['relation'], sentence):
                rel = triple['relation']
            if self._check_if_obj_is_nounish(triple['object'], sentence):
                obj = triple['object']

            if not(sub and rel and obj): # something missing
                continue

            sub, rel, obj = self._replace_words_with_compounds(compounds_ids, sub, rel, obj, sentence)
            subs, sub_support = self._get_supporting_words(sub, sentence, fallbacks=["RB", "PRP"])
            rels, rel_support = self._get_supporting_words(rel, sentence, type="V")
            objs, obj_support = self._get_supporting_words(obj, sentence, fallbacks=["JJ"])
            triples = self._get_all_triples(subs, rels, objs, sub_support, rel_support, obj_support, sentence['sentence'])
            if triples:
                for triple in triples:
                    chosen_triples.append(triple)
        # return chosen_triples
        best_subs = []
        subc = 0
        best_rels = []
        relc = 0
        best_objs = []
        objc = 0
        best_sup = ""
        best_rel = ""
        best_obj = ""
        for triple in chosen_triples:
            cnt = self._get_longest_sup(subc, triple['sub_support'])
            if cnt > subc:
                subc = cnt
                best_subs = triple['sub_support']
            cnt = self._get_longest_sup(relc, triple['rel_support'])
            if cnt > relc:
                relc = cnt
                best_rels = triple['rel_support']
            cnt = self._get_longest_sup(objc, triple['obj_support'])
            if cnt > objc:
                objc = cnt
                best_objs = triple['obj_support']
            best_sup = self._find_longer_string(best_sup, triple['sub'])
            best_rel = self._find_longer_string(best_rel, triple['rel'])
            best_obj = self._find_longer_string(best_obj, triple['obj'])
        if best_sup and best_rel and best_obj:
            return [{'sub': best_sup, 'rel': best_rel, 'obj': best_obj,
                     'sub_support': best_subs, 'rel_support': best_rels, 'obj_support': best_objs}]
        return []

    def _get_longest_sup(self, subc, new_sub):
        cnt = 0
        for k in new_sub:
            cnt += len(new_sub[k])
        if cnt > subc:
            return cnt
        return subc
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
    def _check_if_relation_is_verbish(self, rel, metadata):
        words = rel.split(" ")
        for token in metadata['tokens']:
            for word in words:
                if token['word'] == word and str(token['pos']).startswith("V"):
                    return True
                elif token['word'] != word:
                    continue
        return False

    def _check_if_obj_is_nounish(self, obj, metadata):
        words = obj.split(" ")
        for dep in metadata['dependencies']:
            for word in words:
                if word == dep['dependentGloss'] and dep['dep'] == 'nsubj':
                    return False
        for token in metadata['tokens']:
            for word in words:
                if token['word'] == word and (str(token['pos']).startswith("N") or str(token['pos']).startswith("JJ")):
                    return True
                elif token['word'] != word:
                    continue
        return False


    def _replace_words_with_compounds(self, compounds, sub, rel, obj, sentence):
        index_to_word = {token['index']: token['word'] for token in sentence['tokens']}
        # sub_indexes = {k: v for k, v in index_to_word if v in sub}
        new_sub = self._change_to_word_clusters(index_to_word, sub, compounds)
        new_rel = self._change_to_word_clusters(index_to_word, rel, compounds)
        new_obj = self._change_to_word_clusters(index_to_word, obj, compounds)

        return new_sub, new_rel, new_obj

    def _change_to_word_clusters(self, index_to_word, words, compounds):
        words_clusters = []
        com_idx = []
        for idx, elems in enumerate(compounds):
            for elem in elems:
                if index_to_word[elem] in words:
                    com_idx.append(idx)
                    continue

        # multiple compounds, so the word was duplicated
        # if there is a pair in the sub already, just mark it
        # if not, leave as is (no way to tell)
        if len(set(com_idx)) > 1:
            for idx, elems in enumerate(compounds):
                if com_idx.count(idx) == len(elems): # all words form the elems are in sub
                    string_com = []
                    for elem in elems:
                    #for elem in compounds[com_idx[idx]]:
                        string_com.append(index_to_word[elem])
                    words_clusters.append(" ".join(string_com))
                    if isinstance(words, str):
                        for word in words.split(" "):
                            if word not in string_com:
                                words_clusters.append(word)
                    if isinstance(words, list):
                        for word in words:
                            if word not in string_com:
                                words_clusters.append(word)
                    return words_clusters
            for word in words.split(" "):
                words_clusters.append(word)
            return words_clusters
        elif len(set(com_idx)) == 1:
            string_com = []
            for elem in compounds[com_idx[0]]:
                string_com.append(index_to_word[elem])
            words_clusters.append(" ".join(string_com))
            if isinstance(words, str):
                for word in words.split(" "):
                    if word not in string_com:
                        words_clusters.append(word)
            if isinstance(words, list):
                for word in words:
                    if word not in string_com:
                        words_clusters.append(word)
            return words_clusters
        else:
            if isinstance(words, str):
                for word in words.split(" "):
                    words_clusters.append(word)
            if isinstance(words, list):
                for word in words:
                    words_clusters.append(word)
            return words_clusters





    def _find_longer_string(self, curr_string, candidate_string, type="N"):
        word_count_sub = len(str(candidate_string).split(" "))
        if word_count_sub >= len(curr_string.split(" ")):
            return candidate_string
        return curr_string

    def _update_compound_list(self, id_gov, id_dep, com_ids):
        new_com_ids = com_ids[:]
        for elems in new_com_ids:
            if id_gov in elems:
                elems.append(id_dep)
                return new_com_ids
            if id_dep in elems:
                elems.append(id_gov)
                return new_com_ids
        new_com_ids.append([id_gov, id_dep])
        return new_com_ids

    def _get_compounds_from_words(self, sentence):
        com_ids = []
        for dep in sentence['dependencies']:
            if str(dep['dep']) == 'compound' or str(dep['dep']) == 'aux:pass':
                com_ids = self._update_compound_list(dep['governor'], dep['dependent'], com_ids)

        return com_ids

    def _recurent_find_compound(self, deps_to_conider, to_find= "", found = []):
        com_map = {}
        for dep in deps_to_conider:
            if dep['governor'] not in found and dep['dependent'] not in found:
                if dep['governor'] == to_find or dep['dependent'] == to_find:
                    com_map[dep['governor']] = dep['governorGloss']
                    com_map[dep['dependent']] = dep['dependentGloss']
                    new_to_find = ""
                    if dep['governor'] == to_find:
                        new_to_find = dep['dependent']
                    else:
                        new_to_find = dep['governor']
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
        return com_map

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

    def _get_all_triples(self, subs, rels, objs, sub_support, rel_support, obj_support, sentence):
        if not subs or not rels or not objs:
            print("None correct triples :(")
            return []
        product_triples = product(subs, rels, objs)
        triples = []
        for ptriple in product_triples:
            triple = dict(sub=ptriple[0], rel=ptriple[1], obj=ptriple[2], sub_support=sub_support,
                          rel_support=rel_support, obj_support=obj_support, sentence=sentence)
            triples.append(triple)
        return triples

    def get_triples(self, sentence):
        return self._choose_correct_triples(sentence)
