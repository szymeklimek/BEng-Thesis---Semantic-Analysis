import stanfordnlp
import pandas as pd

nlp = stanfordnlp.Pipeline(processors="tokenize,mwt,lemma,pos")
with open('/Users/aprzybycien/projects/inzynierka/BEng-Thesis---Semantic-Analysis/data/vaccine-articles/txt-format'
          '/article12.txt', encoding="utf-16") as file:
    data = file.read()
doc = nlp(data)
doc.tokens[0].print_tokens()
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


# extract parts of speech
def extract_pos(document):
    parsed_text = {'word': [], 'pos': [], 'exp': []}
    for sent in document.tokens:
        for wrd in sent.words:
            if wrd.pos in pos_dict.keys():
                pos_exp = pos_dict[wrd.pos]
            else:
                pos_exp = 'NA'
            parsed_text['word'].append(wrd.text)
            parsed_text['pos'].append(wrd.pos)
            parsed_text['exp'].append(pos_exp)
    # return a dataframe of pos and text
    return pd.DataFrame(parsed_text)


# extract pos
df = extract_pos(doc)
print(df.head(10))
