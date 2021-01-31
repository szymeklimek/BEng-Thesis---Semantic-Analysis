from stanfordnlp.server import CoreNLPClient


class StanfordAPI:
    annotators = "tokenize, pos, lemma, openie, depparse"

    def get_metadata(self, text):
        with CoreNLPClient(properties={"annotators": self.annotators}, start_server=False, be_quiet=False,
                           timeout=30000, memory='16G') as client:
            # submit the request to the server
            ann = client.annotate(text, properties={"outputFormat": "json", "annotators": self.annotators})
            triples = []
            parsed_text = {'dependencies': [], 'enhancedDependencies': [], 'tokens': []}
            for sentence in ann['sentences']:
                for triple in sentence['openie']:
                    triples.append({
                        'subject': triple['subject'],
                        'relation': triple['relation'],
                        'object': triple['object']
                    })
                # for token in sentence['tokens']:
                # if token['pos'] in POS_TO_DEF.keys():
                #     pos_exp = POS_TO_DEF[token['pos']]
                # else:
                #     pos_exp = 'NA'
                # parsed_text['word'].append(token["word"])
                # parsed_text['pos'].append(token["pos"])
                # parsed_text['exp'].append(pos_exp)
                # parsed_text['lemma'].append(token['lemma'])
                parsed_text['dependencies'] = sentence['basicDependencies']
                parsed_text['enhancedDependencies'] = sentence['enhancedDependencies']
                parsed_text['tokens'] = sentence['tokens']
            parsed_text['sentence'] = text
            parsed_text['triples'] = triples

        return parsed_text