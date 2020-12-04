from src.replace_short_forms import ShortFormReplacer
from src.simple_sentences_algorithm import SimpleSentenceGenerationAlgorithm
from src.stanfordAPI import StanfordAPI
from src.choose_corect_triples import TriplesPicker

class TriplesFinder:
    def create_simple_sentences(self, sentences_metadata):
        ssg = SimpleSentenceGenerationAlgorithm()
        new_metadata = []
        for sentence_meta in sentences_metadata:
            simple_sentences = ssg.get_simple_sentences(sentence_meta)
            new_metadata += simple_sentences
        return new_metadata

    def find_them_triples(self, sentences):
        stanfordAPI = StanfordAPI()
        triples_picker = TriplesPicker()
        metadata = []
        for sentence in sentences:
            sentence = ShortFormReplacer.get_phrase_without_short_form(sentence)
            sentence = sentence.replace('•', '')
            # if sentence.find("says") != -1:
            #     sentence = sentence.split("says")[1]
            if sentence and not sentence.endswith('?'):  # check if empty
                parsed_text = stanfordAPI.get_metadata(sentence)
                metadata.append(parsed_text)
        print("Initial analysis is over. Proceeding to extract simple sentences...")

        only_simple_sentences = self.create_simple_sentences(metadata)
        simple_metadata = []
        print("Created simple sentences. Proceeding to simplified analysis...")
        sentence_count = 0
        triples_count = 0
        for_metamap = []
        for sentence in only_simple_sentences:
            sentence_metadata = stanfordAPI.get_metadata(sentence)
            simple_metadata.append(sentence_metadata)
            sentence_count += 1
            if sentence_metadata['triples']:
                triples_count += 1
            triples_picked = triples_picker.get_triples(sentence_metadata)
            if triples_picked:
                for_metamap.append(triples_picked)

        print("All done. Total sentences count: ", sentence_count, " triples count: ", triples_count)

        only_metadata = simple_metadata
        triples_for_metamap = for_metamap

        return only_metadata, triples_for_metamap