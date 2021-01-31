from src.file_management.filemanager import FileManager
import os
import json
def attach_credilibity(data, credibility):
    for sentence_triples in data:
        for triples in sentence_triples:
            triples['credibility'] = credibility
    return data
os.chdir("../..")
TRIPLES_PATH = os.getcwd() + "/data/articles/triples"

with open(TRIPLES_PATH + "/TRIPLEScredCorpusNONCRED.json") as json_file:
    noncred = json.load(json_file)

with open(TRIPLES_PATH + "/TRIPLEScredCorpusCRED.json") as json_file:
    cred = json.load(json_file)

noncred = attach_credilibity(noncred, 'NONCRED')
cred = attach_credilibity(cred, 'CRED')
sentences = noncred + cred

FileManager.save_to_file(sentences, TRIPLES_PATH + "/TRIPLEScredCorpusALL.json")