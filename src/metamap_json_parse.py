from pymetamap import MetaMap
import os
import json


class App:

    @staticmethod
    def add_mm_context(arg_filepath):
        with open(arg_filepath) as json_file:

            data = json.load(json_file)

            for json_entry in data:

                sentence = list(json_entry.keys())[0]
                triples = list(json_entry.values())[0][0]

                if not triples:
                    continue

                sent_triple_pair = {
                    'sentence': sentence,
                    'triples': triples
                }

                tokens = list(sent_triple_pair['triples'][0].values())
                concepts, error = mm.extract_concepts(tokens)

                print(tokens)

                for concept in concepts:
                    print(concept)
                break


if __name__ == "__main__":

    os.chdir('..')
    metamap_path = os.path.abspath('public_mm/bin/metamap20')
    mm = MetaMap.get_instance(metamap_path)

    filepath = 'data/vaccine-articles/triples/TRIPLESarticle13.json'

    App.add_mm_context(filepath)
