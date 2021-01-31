from src.stanford.stanfordAPI import StanfordAPI


class WordsToLemmasSwitcher:
    def __init__(self):
        self.stanfordAPI = StanfordAPI()

    def generate_lemma_triples(self, all_triples):
        all_new_triples = []
        for triples in all_triples:
            new_triples = []
            for triple in triples:
                sub = self.change_words_to_lemmas(triple['sub'])
                rel = self.change_words_to_lemmas(triple['rel'])
                obj = self.change_words_to_lemmas(triple['obj'])
                sub_support = self.get_lemmatized_supports(triple['sub_support'])
                rel_support = self.get_lemmatized_supports(triple['rel_support'])
                obj_support = self.get_lemmatized_supports(triple['obj_support'])
                new_triples.append({'sub': sub, 'rel': rel, 'obj': obj,
                                    'sub_support': sub_support, 'rel_support': rel_support,
                                    'obj_support': obj_support})
            all_new_triples.append(new_triples)
        return all_new_triples

    def change_words_to_lemmas(self, word):
        metadata = self.stanfordAPI.get_metadata(word)
        lemmatized_word = []
        for token in metadata['tokens']:
            lemmatized_word.append(token['lemma'])
        return " ".join(lemmatized_word)

    def get_lemmatized_supports(self, support):
        new_support = {}
        for k in support:
            new_words = []
            for word in support[k]:
                new_words.append(self.change_words_to_lemmas(word))
            new_support[k] = new_words
        return new_support