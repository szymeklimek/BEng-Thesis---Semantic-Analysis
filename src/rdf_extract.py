from stanfordnlp.server import CoreNLPClient
import re
import os

"""
Extract RDF triples from text.
"""
# dictionary that contains pos tags and their explanations
pos_dict = {
    'CC': 'coordinating conjunction', 'CD': 'cardinal digit', 'DT': 'determiner',
    'EX': 'existential there (like: \"there is\" ... think of it like \"there exists\")',
    'FW': 'foreign word', 'IN': 'preposition/subordinating conjunction', 'JJ': 'adjective \'big\'',
    'JJR': 'adjective, comparative \'bigger\'', 'JJS': 'adjective, superlative \'biggest\'',
    'LS': 'list marker 1)', 'MD': 'modal could, will', 'NN': 'noun, singular \'desk\'',
    'NNS': 'noun plural \'desks\'', 'NNP': 'proper noun, singular \'Harrison\'',
    'NNPS': 'proper noun, plural \'Americans\'', 'PDT': 'predeterminer \'all the kids\'',
    'POS': 'possessive ending parent\'s', 'PRP': 'personal pronoun I, he, she',
    'PRP$': 'possessive pronoun my, his, hers', 'RB': 'adverb very, silently,',
    'RBR': 'adverb, comparative better', 'RBS': 'adverb, superlative best',
    'RP': 'particle give up', 'TO': 'to go \'to\' the store.', 'UH': 'interjection errrrrrrrm',
    'VB': 'verb, base form take', 'VBD': 'verb, past tense took',
    'VBG': 'verb, gerund/present participle taking', 'VBN': 'verb, past participle taken',
    'VBP': 'verb, sing. present, non-3d take', 'VBZ': 'verb, 3rd person sing. present takes',
    'WDT': 'wh-determiner which', 'WP': 'wh-pronoun who, what', 'WP$': 'possessive wh-pronoun whose',
    'WRB': 'wh-abverb where, when', 'QF': 'quantifier, bahut, thoda, kam (Hindi)', 'VM': 'main verb',
    'PSP': 'postposition, common in indian langs', 'DEM': 'demonstrative, common in indian langs'
}


class App:
    @staticmethod
    def extract_triples_and_pos(text):
        with CoreNLPClient(properties={"annotators": "tokenize,pos,lemma,openie"}, start_server=False, be_quiet=False,
                           timeout=30000, memory='16G') as client:
            # submit the request to the server
            ann = client.annotate(text, properties={"outputFormat": "json", "openie.triple.strict": "true"})
            triples = []
            parsed_text = {'word': [], 'pos': [], 'exp': [], 'lemma': []}
            for sentence in ann['sentences']:
                for triple in sentence['openie']:
                    triples.append({
                        'subject': triple['subject'],
                        'relation': triple['relation'],
                        'object': triple['object']
                    })
                for token in sentence['tokens']:
                    if token['pos'] in pos_dict.keys():
                        pos_exp = pos_dict[token['pos']]
                    else:
                        pos_exp = 'NA'
                    parsed_text['word'].append(token["word"])
                    parsed_text['pos'].append(token["pos"])
                    parsed_text['exp'].append(pos_exp)
                    parsed_text['lemma'].append(token['lemma'])

        return [triples, parsed_text]

    @staticmethod
    def load_text_file(path):
        with open(path, encoding="utf-16") as file:
            data = file.read().replace("\n", ". ")
        return data

    @staticmethod
    def save_to_file(doc, path):
        with open(path, "w+") as file:
            for item in doc:
                file.write(str(item) + "\n")


if __name__ == "__main__":
    os.chdir("..")
    ARTICLES_PATH = os.getcwd() + "/data/vaccine-articles/txt-format"
    TRIPLES_PATH = os.getcwd() + "/data/vaccine-articles/triples"
    for roots, dirs, files in os.walk(ARTICLES_PATH):
        for file in files:
            if file.endswith(".txt"):
                print(ARTICLES_PATH + "/" + file)
                data = App.load_text_file(ARTICLES_PATH + "/" + file)
                print(data)
                sentences = re.split("\. |\? |! ]", data)
                all_triples = []
                for sentence in sentences:
                    if sentence:  # check if empty
                        triple = App.extract_triples_and_pos(sentence)
                        all_triples.append({sentence: triple})
                App.save_to_file(all_triples, TRIPLES_PATH + "/TRIPLES" + file)

