import os
import csv
import re

class CredibilityCorpus:
    credible_sentences = []
    neutral_sentences = []
    non_credible_sentences = []

    def __init__(self, path):

        with open(os.getcwd() + path, newline='\n') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                clean_sentences = str(row[3]).replace("“", "").replace("”", "")
                sentences = re.split("\. |\? |! ]", clean_sentences)
                for sentence in sentences:
                    if row[5] == 'CRED':
                        self.credible_sentences.append(sentence)
                    elif row[5] == 'NEU':
                        self.neutral_sentences.append(sentence)
                    elif row[5] == 'NONCRED':
                        self.non_credible_sentences.append(sentence)
        print("CRED count: ", len(self.credible_sentences),
              "NEU count: ", len(self.neutral_sentences),
              "NONCRED count:", len(self.non_credible_sentences))

    def get_credible_sentences(self):
        return self.credible_sentences

