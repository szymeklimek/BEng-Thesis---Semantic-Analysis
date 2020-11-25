class TriplesFromOpenieGenerator:

    def _choose_correct_triple(self, sentence):
        # todo: get supporting words based on dependencies
        if sentence['triples']:
            return sentence['triples']
        else:
            print("Openie could not find a triple ;(")
            return {}

    def get_triple(self, sentence):
        return self._choose_correct_triple(sentence)
