import os
from src.triples_finder import TriplesFinder
SCORE_MATCH_DIRECT = 1
SCORE_MATCH_SUPPORT = 0.7  # not used
SUB_THRESHOLD = 0.5

def compare_sentences(first_triples, second_triples):
    main_score = 0
    sup_score = 0
    # how many triples should match for perfect score
    perfect_match = len(first_triples) if len(first_triples) > len(second_triples) else len(second_triples)
    for triple in first_triples:
        for triple2 in second_triples:
            triples_main_score = compare_main_triples(*triple, *triple2)
            main_score += triples_main_score
            triples_sub_score = compare_sub_triples(*triple, *triple2)
            # adding support threshold only makes sense if main part of triples are similar
            if triples_main_score > SUB_THRESHOLD:
                sup_score += triples_sub_score
    main_score = main_score/perfect_match
    sup_score = sup_score/perfect_match
    whole_score = (main_score + sup_score)/2
    return main_score, sup_score, whole_score

def compare_main_triples(first_triple, second_triple):
    tscore = 0
    if first_triple['sub'] == second_triple['sub']:
        tscore += SCORE_MATCH_DIRECT
    if first_triple['rel'] == second_triple['rel']:
        tscore += SCORE_MATCH_DIRECT
    if first_triple['obj'] == second_triple['obj']:
        tscore += SCORE_MATCH_DIRECT
    if tscore > 0:
        tscore = tscore/3

    return tscore

def compare_sub_triples(first_triple, second_triple):
    sscore = 0
    # sup_support2 = second_triple['sub_support'].values()[:]
    # for sup_support in first_triple['sub_support'].values():
    #     if sup_support in sup_support2:
    #         sscore += SCORE_MATCH_SUPPORT
    sub1_values_squashed = [elem[0] for elem in first_triple['sub_support'].values()]
    sub2_values_squashed = [elem[0] for elem in second_triple['sub_support'].values()]
    matched_count = len(list(set(sub1_values_squashed) & set(sub2_values_squashed)))
    total_sup_support_count = len(set(sub1_values_squashed + sub2_values_squashed))
    sub_support_intersection_score = matched_count/total_sup_support_count if total_sup_support_count > 0 else 1
    sscore += sub_support_intersection_score

    rel1_values_squashed = [elem[0] for elem in first_triple['rel_support'].values()]
    rel2_values_squashed = [elem[0] for elem in second_triple['rel_support'].values()]
    matched_count = len(list(set(rel1_values_squashed) & set(rel2_values_squashed)))
    total_rel_support_count = len(set(rel1_values_squashed + rel2_values_squashed))
    rel_support_intersection_score = matched_count / total_rel_support_count if total_rel_support_count > 0 else 1
    sscore += rel_support_intersection_score

    obj1_values_squashed = [elem[0] for elem in first_triple['obj_support'].values()]
    obj2_values_squashed = [elem[0] for elem in second_triple['obj_support'].values()]
    matched_count = len(list(set(obj1_values_squashed) & set(obj2_values_squashed)))
    total_obj_support_count = len(set(obj1_values_squashed + obj2_values_squashed))
    obj_support_intersection_score = matched_count / total_obj_support_count if total_obj_support_count > 0 else 1
    sscore += obj_support_intersection_score

    sscore = sscore/3
    return sscore

if __name__ == "__main__":
    os.chdir("..")
    triples_finder = TriplesFinder()
    with open('data/compare_triples/sentence1.txt') as file:
        first_sentence = file.read()
        only_metadata, first_sentence_triples = triples_finder.find_them_triples([first_sentence])
    with open('data/compare_triples/sentence2.txt') as file:
        second_sentence = file.read()
        only_metadata, second_sentence_triples = triples_finder.find_them_triples([second_sentence])

    score, sub_score, whole_score = compare_sentences(first_sentence_triples, second_sentence_triples)
    print("Sentence1: ", first_sentence)
    print("Sentence2: ", second_sentence)
    print("Main Score: ", score*100, "%")
    print("Sub score: ", sub_score*100, "%")
    print("Whole score: ", whole_score*100, "%")
    print(first_sentence_triples)
    print(second_sentence_triples)
