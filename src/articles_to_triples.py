import os
from src.filemanager import FileManager
from src.triples_finder import TriplesFinder
from src.parse_credibility_corpus import CredibilityCorpus
from src.stanfordAPI import StanfordAPI
import re


def generate_lemma_triples(all_triples):
    all_new_triples = []
    for triples in all_triples:
        new_triples = []
        for triple in triples:
            sub = change_words_to_lemmas(triple['sub'])
            rel = change_words_to_lemmas(triple['rel'])
            obj = change_words_to_lemmas(triple['obj'])
            sub_support = get_lemmatized_supports(triple['sub_support'])
            rel_support = get_lemmatized_supports(triple['rel_support'])
            obj_support = get_lemmatized_supports(triple['obj_support'])
            new_triples.append({'sub': sub, 'rel': rel, 'obj': obj,
                                'sub_support': sub_support, 'rel_support': rel_support, 'obj_support': obj_support})
        all_new_triples.append(new_triples)
    return all_new_triples


def change_words_to_lemmas(word):
    stanfordapi = StanfordAPI()
    metadata = stanfordapi.get_metadata(word)
    lemmatized_word = []
    for token in metadata['tokens']:
        lemmatized_word.append(token['lemma'])
    return " ".join(lemmatized_word)


def get_lemmatized_supports(support):
    new_support = {}
    for k in support:
        new_words = []
        for word in support[k]:
            new_words.append(change_words_to_lemmas(word))
        new_support[k] = new_words
    return new_support

if __name__ == "__main__":
    os.chdir("..")
    ARTICLES_PATH = os.getcwd() + "/data/vaccine-articles/txt-format"
    TRIPLES_PATH = os.getcwd() + "/data/vaccine-articles/triples"
    triples_finder = TriplesFinder()

    # articles
    # for roots, dirs, files in os.walk(ARTICLES_PATH):
    #     for file in files:
    #         if file.endswith(".txt"):
    #             print(ARTICLES_PATH + "/" + file)
    #             data = FileManager.load_text_file(ARTICLES_PATH + "/" + file)
    #             print(data)
    #             sentences = re.split("\. |\? |! ]", data)
    #             only_metadata, triples_for_metamap = find_them_triples(sentences)
    #
    #             FileManager.save_to_file(only_metadata, TRIPLES_PATH + "/TRIPLESMETA" + file.split(".")[0] + ".json")
    #             FileManager.save_to_file(triples_for_metamap, TRIPLES_PATH + "/TRIPLES" + file.split(".")[0] + ".json")
    # credibility corpus
    #crecCorpus = CredibilityCorpus(r"/data/vaccine-articles/credibility-corpus/sentences.csv")
    crecCorpus = CredibilityCorpus(r"/data/vaccine-articles/credibility-corpus/similar-sentences.csv",
                                   credibilityCorpus=False)
    #sentences = crecCorpus.get_credible_sentences()
    sentences = crecCorpus.get_credible_sentences()
    only_metadata, triples_for_metamap = triples_finder.find_them_triples(sentences)
    lemmatized_triples = generate_lemma_triples(triples_for_metamap)

    FileManager.save_to_file(only_metadata, TRIPLES_PATH + "/TRIPLESMETAcredCorpusCRED.json")
    FileManager.save_to_file(triples_for_metamap, TRIPLES_PATH + "/TRIPLEScredCorpusCRED.json")
    print(only_metadata)
    print(triples_for_metamap)
