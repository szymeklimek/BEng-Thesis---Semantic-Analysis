import os
from src.replace_short_forms import ShortFormReplacer
from src.stanfordAPI import StanfordAPI
from src.filemanager import FileManager
import re

if __name__ == "__main__":
    os.chdir("..")
    ARTICLES_PATH = os.getcwd() + "/data/vaccine-articles/txt-format"
    TRIPLES_PATH = os.getcwd() + "/data/vaccine-articles/triples"
    stanfordAPI = StanfordAPI()
    for roots, dirs, files in os.walk(ARTICLES_PATH):
        for file in files:
            if file.endswith("article13.txt"):
                print(ARTICLES_PATH + "/" + file)
                data = FileManager.load_text_file(ARTICLES_PATH + "/" + file)
                print(data)
                sentences = re.split("\. |\? |! ]", data)
                all_triples = []
                for sentence in sentences:
                    sentence = ShortFormReplacer.get_phrase_without_short_form(sentence)
                    sentence = sentence.replace('•', '')
                    if sentence and not sentence.endswith('?'):  # check if empty
                        parsed_text = stanfordAPI.get_metadata(sentence)
                        all_triples.append(parsed_text)
                json_all_triples = all_triples
                FileManager.save_to_file(json_all_triples, TRIPLES_PATH + "/TRIPLESMETA" + file.split(".")[0] + ".json")
