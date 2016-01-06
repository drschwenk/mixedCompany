from fuzzywuzzy import fuzz, process
from collections import defaultdict
from itertools import permutations


def match_ingredients(recipe, comp_ing_dict):
    sanitzed_comp_ing = {k.decode('utf-8'): v for k, v in comp_ing_dict.iteritems()}
    matches = []
    for ing in recipe:
        match_list = process.extractBests(ing, sanitzed_comp_ing.keys(), scorer=fuzz.token_set_ratio, score_cutoff=80)
        matches+= [match[0] for match in match_list]
    return list(set(matches))


def compute_single_avg_weight(recipe, comp_ing_dict, edge_dict):
    """
    computes the average weight of the ingredients in a recipe
    :param recipe single list of ingredients
    :param comp_ing_dict compound ingredient dictionary
    :param edge_dict: dict of edges comprising the flavor network
    :return: avg weight of this recipe
    """
    pairwise_combos = list(permutations(match_ingredients(recipe, comp_ing_dict), 2))
    tot_weight = 0
    norm_factor = float(2) / (len(recipe)*(len(recipe)-1))
    # I compute permutations here because there's no way to know how the ingredients are ordered in the edge dict keys
    edge_ids = []
    for ing_pair in pairwise_combos:
        edge_ids.append(ing_pair[0] + ', ' + ing_pair[1])

    for edge_id in edge_ids:
        tot_weight += edge_dict[edge_id]

    return tot_weight * norm_factor


def compute_all_weights(recipe_dict, comp_ing_dict, edge_list):
    edge_dict = defaultdict(int)
    recipe_weights = defaultdict(float)
    for edge in edge_list:
        n1 = edge.dst_vid
        n2 = edge.src_vid
        key = n1+', '+n2
        edge_dict[key] = edge.attr['weight']

    for recipe_name, ingredients in recipe_dict.iteritems():
        recipe_weights[recipe_name] = compute_single_avg_weight(ingredients, comp_ing_dict, edge_dict)

    return edge_dict

