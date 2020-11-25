import os
from src.replace_short_forms import ShortFormReplacer
from src.stanfordAPI import StanfordAPI
from src.filemanager import FileManager
from src.simple_sentences_algorithm import SimpleSentenceGenerationAlgorithm
import re


def create_simple_sentences(sentences_metadata):
    ssg = SimpleSentenceGenerationAlgorithm()
    new_metadata = []
    for sentence_meta in sentences_metadata:
        simple_sentences = ssg.get_simple_sentences(sentence_meta)
        new_metadata += simple_sentences
    return new_metadata


if __name__ == "__main__":
    os.chdir("..")
    ARTICLES_PATH = os.getcwd() + "/data/vaccine-articles/txt-format"
    TRIPLES_PATH = os.getcwd() + "/data/vaccine-articles/triples"
    stanfordAPI = StanfordAPI()
    for roots, dirs, files in os.walk(ARTICLES_PATH):
        for file in files:
            if file.endswith(".txt"):
                print(ARTICLES_PATH + "/" + file)
                data = FileManager.load_text_file(ARTICLES_PATH + "/" + file)
                print(data)
                sentences = re.split("\. |\? |! ]", data)
                metadata = []
                for sentence in sentences:
                    sentence = ShortFormReplacer.get_phrase_without_short_form(sentence)
                    sentence = sentence.replace('•', '')
                    if sentence and not sentence.endswith('?'):  # check if empty
                        parsed_text = stanfordAPI.get_metadata(sentence)
                        metadata.append(parsed_text)
                print("Initial analysis is over. Proceeding to extract simple sentences...")
                only_simple_sentences = create_simple_sentences(metadata)
                simple_metadata = []
                print("Created simple sentences. Proceeding to simplified analysis...")
                sentence_count = 0
                triples_count = 0
                for sentence in only_simple_sentences:
                    parsed_text = stanfordAPI.get_metadata(sentence)
                    simple_metadata.append(parsed_text)
                    sentence_count += 1
                    if parsed_text['triples']:
                        triples_count += 1

                print("All done. Total sentences count: ", sentence_count, " triples count: ", triples_count)

                json_all_triples = simple_metadata

                FileManager.save_to_file(json_all_triples, TRIPLES_PATH + "/TRIPLESMETA" + file.split(".")[0] + ".json")
