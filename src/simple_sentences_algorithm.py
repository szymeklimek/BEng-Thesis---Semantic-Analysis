class SimpleSentenceGenerationAlgorithm:

    def _check_if_found(self, found, idx_gov, idx_dep):
        if idx_gov in found or idx_dep in found:
            return True
        return False

    def _get_subj_indexes(self, sentence):
        sub_indexes = []
        for idx, dep in enumerate(sentence['dependencies']):
            if 'nsubj' in str(dep['dep']):
                sub_indexes.append(idx)
        return sub_indexes

    def _check_if_simple_sentence(self, sub_count):
        if len(sub_count) == 1:
            return True
        return False

    def _reccurent_find_all(self, deps_to_consider, found=[], to_find=[]):
        deps = []
        temp_deps_to_consider = deps_to_consider[:]
        for idx, dep in enumerate(temp_deps_to_consider):
            if dep['governor'] in to_find or dep['dependent'] in to_find:
                if not self._check_if_found(found, dep['governor'], dep['dependent']):
                    deps.append(dep)
                    new_deps_to_consider = temp_deps_to_consider[:]
                    new_deps_to_consider.pop(idx)
                    to_find_idx = 0
                    if dep['governor'] in to_find:
                        to_find_idx = dep['dependent']
                    else:
                        to_find_idx = dep['governor']
                    more_deps = self._reccurent_find_all(new_deps_to_consider, to_find, [to_find_idx])
                    if more_deps:
                        deps = deps + more_deps
        return deps

    def _find_connected_deps(self, sub, deps_to_consider):
        gov_id = sub['governor']
        dep_id = sub['dependent']
        deps = []
        idx_sub = 0
        temp_deps_to_consider = deps_to_consider[:]
        for idx, dep in enumerate(deps_to_consider):
            if dep['governor'] == sub['governor'] and dep['dependent'] == sub['dependent']:
                idx_sub = idx
        temp_deps_to_consider.pop(idx_sub)
        deps = self._reccurent_find_all(temp_deps_to_consider, to_find=[gov_id, dep_id])
        deps.append(sub)
        return deps

    def _get_dependencies_tree_from_compound(self, sentence, sub_indexes):
        deps_to_consider = []
        for dep in sentence['dependencies']:
            if str(dep['dep']) not in ['mark', 'acl', 'appos', 'advcl', 'cc', 'ccomp', 'conj', 'dep', 'parataxis',
                                       'ref', 'punct', 'acl:relcl', 'det']:
                deps_to_consider.append(dep)
        # build deps trees for nsubjs
        dependencies = []
        for sub_idx in sub_indexes:
            sub = sentence['dependencies'][sub_idx]
            dependencies.append(self._find_connected_deps(sub, deps_to_consider))
        return dependencies

    def _glue_words_into_sentences(self, dependencies):
        index_to_word = {}
        for deps in dependencies:
            if deps['governor'] > 0:
                index_to_word[deps['governor']] = deps['governorGloss']
            if deps['dependent'] > 0:
                index_to_word[deps['dependent']] = deps['dependentGloss']

        ordered_words = [index_to_word[k] for k in sorted(index_to_word)]
        return " ".join(ordered_words)


    def get_simple_sentences(self, sentence):
        simple_sentences = []
        sub_indexes = self._get_subj_indexes(sentence)
        simple_sentence_deps = self._get_dependencies_tree_from_compound(sentence, sub_indexes)
        for deps in simple_sentence_deps:
            sentence = self._glue_words_into_sentences(deps)
            simple_sentences.append(sentence)

        return simple_sentences

