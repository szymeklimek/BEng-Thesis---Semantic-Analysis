class TriplesFromDependenciesGenerator:
    def _get_pos_of_word(self, sentence, word):
        for token in sentence['tokens']:
            if token['word'] == word:
                return token['pos']

    # it takes only simple sentences
    def get_triple(self, sentence):
        sub = ""
        rel = ""
        obj = ""
        sub_addons = {}
        rel_addons = {}
        obj_addons = {}
        is_cop = False
        cop = ""
        for dep in sentence['dependencies']:

            if dep['dep'] == 'nsubj':
                pos = self._get_pos_of_word(sentence, dep['governorGloss'])
                if not str(pos).startswith('V'):
                    obj = dep['governorGloss']
                    sub = dep['dependentGloss']
                    is_cop = True
                else:
                    rel = dep['governorGloss']  # ?
                    sub = dep['dependentGloss']
                continue
            if dep['dep'] == 'nsubj:pass':
                sub = dep['dependentGloss']
                continue
            if dep['dep'] == 'aux:pass':
                rel = str(dep['dependentGloss']) + " " + str(dep['governorGloss'])
            if dep['dep'] == 'nmod':
                if obj:
                    obj = obj + " " + dep['dependentGloss']
                else:
                    obj = dep['dependentGloss']
                continue
            if dep['dep'] == 'cop':
                cop = dep['dependentGloss']
                continue
            if dep['dep'] == 'obl':
                obj = dep['dependentGloss'] + " " + obj
                continue
            if 'obj' in str(dep['dep']):
                obj = dep['governorGloss']
                continue
            # normally in nsubj governor = verb (rel), dependent = subject and obj is object, if governor is not a verb
            # then governor = object, dependent = subject and cop is the rel
        if is_cop:
            rel = cop
        return {'sub': sub, 'rel': rel, 'obj': obj}