class TriplesFromDependenciesGenerator:
    def _get_pos_of_word(self, sentence, word):
        for token in sentence['tokens']:
            if token['word'] == word:
                return token['pos']

    def _add_dependant(self, dep, words_list):
        if dep['dependentGloss'] not in words_list:
            words_list.append(dep['dependentGloss'])
        return words_list

    def _add_governor(self, dep, words_list):
        if dep['governorGloss'] not in words_list:
            words_list.append(dep['governorGloss'])
        return words_list

    def _add_list_to_support(self, unassigned_support, key):
        if key not in unassigned_support.keys():
            unassigned_support[key] = []
        return unassigned_support

    # it takes only simple sentences
    def get_triple(self, sentence):
        sub = []
        rel = []
        obj = []
        sub_addons = []
        rel_addons = []
        obj_addons = []
        component_words = {}
        unassigned_support = {}
        deps_to_consider = []
        for dep in sentence['dependencies']:
            if dep['dep'] not in ['cc', 'dep', 'det', 'discourse', 'nn', 'parataxis', 'pcomp', 'xsubj', 'xsubj']:
                deps_to_consider.append(dep)
        for dep in deps_to_consider:
            if dep['dep'] == 'acomp':
                rel = self._add_governor(dep, rel)
                obj = self._add_dependant(dep, obj)

            elif dep['dep'] == 'advcl':
                rel = self._add_governor(dep, rel)
                rel_addons = self._add_dependant(dep, rel_addons)

            elif dep['dep'] == 'advmod':
                unassigned_support = self._add_list_to_support(unassigned_support, dep['governorGloss'])
                unassigned_support[dep['governorGloss']] = \
                    self._add_dependant(dep, unassigned_support[dep['governorGloss']])
                rel = self._add_governor(dep, rel)

            elif dep['dep'] == 'agent':
                rel = self._add_governor(dep, rel)
                obj = self._add_dependant(dep, obj)

            elif dep['dep'] == 'amod':
                unassigned_support = self._add_list_to_support(unassigned_support, dep['governorGloss'])
                unassigned_support[dep['governorGloss']] = \
                    self._add_dependant(dep, unassigned_support[dep['governorGloss']])

            elif dep['dep'] == 'appos':
                unassigned_support = self._add_list_to_support(unassigned_support, dep['governorGloss'])
                unassigned_support[dep['governorGloss']] = \
                    self._add_dependant(dep, unassigned_support[dep['governorGloss']])

            elif dep['dep'] == 'aux':
                rel = self._add_dependant(dep, rel)
                rel = self._add_governor(dep, rel)

            elif dep['dep'] == 'ccomp':
                rel = self._add_governor(dep, rel)
                obj = self._add_dependant(dep, obj)

            elif dep['dep'] == 'conj':
                unassigned_support = self._add_list_to_support(unassigned_support, dep['governorGloss'])
                unassigned_support[dep['governorGloss']] = \
                    self._add_dependant(dep, unassigned_support[dep['governorGloss']])
                #
                # unassigned_support = self._add_list_to_support(unassigned_support, dep['dependantGloss'])
                # unassigned_support[dep['dependantGloss']] = \
                #     self._add_dependant(dep, unassigned_support[dep['governorGloss']])

            elif dep['dep'] == 'cop':
                rel = self._add_dependant(dep, rel)
                obj = self._add_governor(dep, obj)

            elif dep['dep'] == 'csubj':
                rel = self._add_governor(dep, rel)
                sub = self._add_dependant(dep, sub)

            elif dep['dep'] == 'csubj:pass':
                rel = self._add_governor(dep, rel)
                sub = self._add_dependant(dep, sub)

            elif dep['dep'] == 'dobj':
                rel = self._add_governor(dep, rel)
                obj = self._add_dependant(dep, obj)

            elif dep['dep'] == 'expl':
                rel = self._add_governor(dep, rel)
                sub = self._add_dependant(dep, sub)

            elif dep['dep'] == 'iobj':
                rel = self._add_governor(dep, rel)
                obj_addons = self._add_dependant(dep, obj_addons)

            elif dep['dep'] == 'mark':
                obj_addons = self._add_governor(dep, obj_addons)
                obj_addons = self._add_dependant(dep, obj_addons)

            elif dep['dep'] == 'neg':
                unassigned_support = self._add_list_to_support(unassigned_support, dep['governorGloss'])
                unassigned_support[dep['governorGloss']] = \
                    self._add_dependant(dep, unassigned_support[dep['governorGloss']])

            elif dep['dep'] == 'nsubj':
                rel = self._add_governor(dep, rel)
                sub = self._add_dependant(dep, sub)

            elif dep['dep'] == 'nsubj:pass':
                rel = self._add_governor(dep, rel)
                sub = self._add_dependant(dep, sub)

            elif dep['dep'] == 'number' or dep['dep'] == 'npadvmod' or dep['dep'] == 'mwe' or dep['dep'] == 'goeswith' or \
                    dep['dep'] == 'component':
                component_words = self._add_list_to_support(component_words, dep['dependentGloss'])
                component_words[dep['dependentGloss']] = \
                    self._add_dependant(dep, component_words[dep['dependentGloss']])

            elif dep['dep'] == 'num':
                unassigned_support = self._add_list_to_support(unassigned_support, dep['governorGloss'])
                unassigned_support[dep['governorGloss']] = \
                    self._add_dependant(dep, unassigned_support[dep['governorGloss']])

            elif dep['dep'] == 'pobj':
                unassigned_support = self._add_list_to_support(unassigned_support, dep['dependentGloss'])
                unassigned_support[dep['dependentGloss']] = \
                    self._add_dependant(dep, unassigned_support[dep['dependentGloss']])

            elif dep['dep'] == 'vmod':
                rel_addons = self._add_governor(dep, rel_addons)
                rel = self._add_dependant(dep, rel)

            elif dep['dep'] == 'xcomp':
                rel = self._add_dependant(dep, rel)
                rel_addons = self._add_dependant(dep, rel_addons)


        sub, sub_addons = self._make_words_complete(sub, sub_addons, unassigned_support, component_words)
        rel, rel_addons = self._make_words_complete(rel, rel_addons, unassigned_support, component_words)
        obj, obj_addons = self._make_words_complete(obj, obj_addons, unassigned_support, component_words)

        sub_addons = self._make_words_complete(sub_addons, [], unassigned_support, component_words, is_support=True)
        rel_addons = self._make_words_complete(rel_addons, [], unassigned_support, component_words, is_support=True)
        obj_addons = self._make_words_complete(obj_addons, [], unassigned_support, component_words, is_support=True)
        # todo: make the dicts from list

        sub_text = self._order_words(sub, sentence)
        rel_text = self._order_words(rel, sentence)
        obj_text = self._order_words(obj, sentence)

        return {'sub': sub_text, 'rel': rel_text, 'obj': obj_text,
                'sup_support': sub_addons, 'rel_support': rel_addons, 'obj_support': obj_addons}

    def _order_words(self, words, metadata):
        index_to_word = {}
        for token in metadata['tokens']:
            if token['word'] in words:
                index_to_word[token['index']] = token['word']

        ordered_words = [index_to_word[k] for k in sorted(index_to_word)]
        return " ".join(ordered_words)

    def _make_words_complete(self, word_list, word_addons, unassigned_support, component_words, is_support=False):
        new_words = word_list[:]
        for sub_word in word_list:
            if sub_word in unassigned_support.keys():
                if not is_support:
                    word_addons.append(unassigned_support[sub_word])
                else:
                    new_words.append(unassigned_support[sub_word])
                del unassigned_support[sub_word]
            if sub_word in component_words.keys():
                new_words.remove(sub_word)
                new_words.append(sub_word + component_words[sub_word])
        return new_words, word_addons

    # def get_triple(self, sentence):
    #     sub = ""
    #     rel = ""
    #     obj = ""
    #     sub_addons = {}
    #     rel_addons = {}
    #     obj_addons = {}
    #     is_cop = False
    #     is_passive = False
    #     cop = ""
    #     for dep in sentence['dependencies']:
    #
    #         if dep['dep'] == 'nsubj':
    #             pos = self._get_pos_of_word(sentence, dep['governorGloss'])
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
