import os
import csv
import re

class CredibilityCorpus:
    credible_sentences = []
    neutral_sentences = []
    non_credible_sentences = []
    vaccines_sentences = []

    def __init__(self, path, credibilityCorpus=True):

        with open(os.getcwd() + path, newline='\n') as csv_file:
            names = []
            reader = csv.reader(csv_file, delimiter=',')
            if(credibilityCorpus):
                self.read_credibility_corpus(reader)
            else:
                self.read_similar_sentences(reader)

    def read_credibility_corpus(self, reader):
        names = []
        for row in reader:
            clean_sentences = str(row[3]).replace("“", "").replace("”", "")
            sentences = re.split("\. |\? |! ]", clean_sentences)
            for sentence in sentences:
                if row[4] not in names:
                    names.append(row[4])
                if row[4] == 'vaccination' and row[5] == 'NONCRED':
                    self.vaccines_sentences.append(sentence)
                if row[5] == 'CRED':
                    self.credible_sentences.append(sentence)
                elif row[5] == 'NEU':
                    self.neutral_sentences.append(sentence)
                elif row[5] == 'NONCRED':
                    self.non_credible_sentences.append(sentence)
        print("CRED count: ", len(self.credible_sentences),
              "NEU count: ", len(self.neutral_sentences),
              "NONCRED count:", len(self.non_credible_sentences),
              "vaccine count:", len(self.vaccines_sentences),
              "categories: ", names)
    def read_similar_sentences(self, reader):
        for row in reader:
            clean_sentences = str(row[1]).replace("“", "").replace("”", "").replace('\'', "")
            sentences = re.split("\. |\? |! ]", clean_sentences)
            for sentence in sentences:
                if row[0] == 'CRED':
                    self.credible_sentences.append(sentence)
                elif row[0] == 'NEU':
                    self.neutral_sentences.append(sentence)
                elif row[0] == 'NONCRED':
                    self.non_credible_sentences.append(sentence)
        print("CRED count: ", len(self.credible_sentences),
              "NEU count: ", len(self.neutral_sentences),
              "NONCRED count:", len(self.non_credible_sentences))

    def get_credible_sentences(self):
        return self.credible_sentences

    def get_vaccine_sentences(self):
        return self.vaccines_sentences

    def get_non_credible_sentences(self):
        return self.non_credible_sentences

