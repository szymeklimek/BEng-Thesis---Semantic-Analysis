import os
from src.filemanager import FileManager
from src.triples_finder import TriplesFinder
from src.parse_credibility_corpus import CredibilityCorpus
import re

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
    crecCorpus = CredibilityCorpus(r"/data/vaccine-articles/credibility-corpus/sentences.csv")
    sentences = crecCorpus.get_credible_sentences()
    only_metadata, triples_for_metamap = triples_finder.find_them_triples(sentences)
    FileManager.save_to_file(only_metadata, TRIPLES_PATH + "/TRIPLESMETAcredCorpus.json")
    FileManager.save_to_file(triples_for_metamap, TRIPLES_PATH + "/TRIPLEScredCorpus.json")
    print(only_metadata)
    print(triples_for_metamap)
