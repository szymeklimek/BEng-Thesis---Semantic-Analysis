import os
import re

from src.file_management.filemanager import FileManager
from src.stanford.triples_selector.triples_finder import TriplesFinder
from src.text_parsing.parse_credibility_corpus import CredibilityCorpus
from src.stanford.words_to_lemmas_switcher import WordsToLemmasSwitcher

PATH_TO_ARTICLES = "/data/articles/txt-format"
PATH_TO_CREDIBILITY_CORPUS = "/data/articles/credibility-corpus/sentences.csv"
PATH_TO_SIMILAR_SENTENCES = "/data/articles/credibility-corpus/similar-sentences.csv"
PATH_TO_TRIPLES = "/data/articles/triples"


class SentencesParser:
    def __init__(self):
        os.chdir("..")
        self.ARTICLES_PATH = os.getcwd() + PATH_TO_ARTICLES
        self.TRIPLES_PATH = os.getcwd() + PATH_TO_TRIPLES
        self.PATH_TO_CREDIBILITY_COPRUS = os.getcwd() + PATH_TO_CREDIBILITY_CORPUS
        self.PATH_TO_SIMILAR_SENTENCES = os.getcwd() + PATH_TO_SIMILAR_SENTENCES
        self.triples_finder = TriplesFinder()
        self.words_to_lemmas_switcher = WordsToLemmasSwitcher()

    def parse_article(self, article_name):
        if not article_name.endswith(".txt"):
            article_name = article_name + ".txt"
        self._generate_triples_for_text(article_name)

    def parse_all_articles(self):
        for roots, dirs, files in os.walk(self.ARTICLES_PATH):
            for file in files:
                if file.endswith(".txt"):
                    self._generate_triples_for_text(file)

    def _generate_triples_for_text(self, file):
        file_path = "{}/{}".format(self.ARTICLES_PATH, file)
        print(file_path)
        data = FileManager.load_text_file(file_path)
        print(data)
        sentences = self._split_text_into_sentences(data)
        only_metadata, triples_for_metamap = self.triples_finder.find_them_triples(sentences)
        lemmatized_triples = self.words_to_lemmas_switcher.generate_lemma_triples(triples_for_metamap)

        FileManager.save_to_file(only_metadata,
                                 "{0}/TRIPLESMETA{1}.json".format(self.TRIPLES_PATH, file.split(".")[0]))
        FileManager.save_to_file(triples_for_metamap,
                                 "{0}/TRIPLES{1}.json".format(self.TRIPLES_PATH, file.split(".")[0]))
        FileManager.save_to_file(lemmatized_triples,
                                 "{0}/LEMMATRIPLES{1}.json".format(self.TRIPLES_PATH, file.split(".")[0]))

    def _split_text_into_sentences(self, text):
        return re.split("\. |\? |! ]", text)

    def parse_credibility_corpus(self):
        crecCorpus = CredibilityCorpus(self.PATH_TO_CREDIBILITY_COPRUS,
                                       credibilityCorpus=True)
        # todo: automate choice of saving with credibility label
        # todo: automate parsing chosen types of sentences
        sentences = crecCorpus.get_credible_sentences()
        only_metadata, triples_for_metamap = self.triples_finder.find_them_triples(sentences)
        wordsToLemmasSwitcher = WordsToLemmasSwitcher()
        lemmatized_triples = wordsToLemmasSwitcher.generate_lemma_triples(triples_for_metamap)

        FileManager.save_to_file(only_metadata, self.TRIPLES_PATH + "/TRIPLESMETAcredCorpusCRED.json")
        FileManager.save_to_file(triples_for_metamap, self.TRIPLES_PATH + "/TRIPLEScredCorpusCRED.json")
        FileManager.save_to_file(lemmatized_triples, self.TRIPLES_PATH + "/TRIPLEScredCorpusLEMMASCRED.json")
        print(only_metadata)
        print(triples_for_metamap)
        return None


if __name__ == "__main__":
    print("Sentences to triples program starting...")
    print("Default path for articles: {}".format(PATH_TO_ARTICLES))
    print("If You would like to parse one file, enter the name of the text file + <enter>.\n"
          "Press <enter> if You would like to parse all of them.\n"
          "If You don't want to parse any articles, type <space> + <enter>")
    article_answer = input()
    parse_all = False
    article_to_parse = ""
    if article_answer == "":
        parse_all = True
    elif article_answer == " ":
        article_to_parse = ""
    else:
        article_to_parse = article_answer
    print("Default path for credibility corpus: {}".format(PATH_TO_CREDIBILITY_CORPUS))
    print("Would You like to parse credibilityCorpus?\n"
          "Choose y/n.")
    corpus_answer = input()
    parse_cred_corpus = False
    if corpus_answer == 'y':
        parse_cred_corpus = True
    elif corpus_answer == 'n':
        parse_cred_corpus = False
    else:
        print("Unsupported option, falling to default. Will not parse credibility corpus.")

    sentences_parser = SentencesParser()
    if parse_all:
        sentences_parser.parse_all_articles()
    if article_to_parse != "":
        sentences_parser.parse_article(article_to_parse)
    if parse_cred_corpus:
        sentences_parser.parse_credibility_corpus()
