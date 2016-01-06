from fuzzywuzzy import fuzz, process
from collections import defaultdict
from itertools import permutations
import cPickle as pickle
import itertools

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
    """

    :param recipe_dict: dictionary of cocktail recipes
    :param comp_ing_dict: flavor component : ingredient_dict
    :param edge_list:
    :return:
    """
    # edge_dict = defaultdict(int)
    edge_dict = edge_list
    recipe_weights = defaultdict(float)
    # for edge in edge_list:
    #     n1 = edge.dst_vid
    #     n2 = edge.src_vid
    #     key = n1+', '+n2
    #     edge_dict[key] = edge.attr['weight']

    for recipe_name, ingredients in recipe_dict.iteritems():
        recipe_weights[recipe_name] = compute_single_avg_weight(ingredients, comp_ing_dict, edge_dict)

    return recipe_weights

if __name__ == '__main__':
    with open('./backbone_edges_dict.pkl') as f:
        edge_dict = pickle.load(f)
    with open('./data/second_ing_flav_dict.pkl', 'r') as f:
        comp_ing_dict = pickle.load(f)
    with open('./data/comb_recipes.pkl', 'r') as f:
        comb_recipes = pickle.load(f)

    def get_range(dictionary, begin, end):
        return dict(itertools.islice(dictionary.iteritems(), begin, end+1))

    weight_dict = compute_all_weights(get_range(comb_recipes, 0, 10), comp_ing_dict, edge_dict)

    with open('./avg_recipe_weights.pkl', 'w') as f:
        pickle.dump(weight_dict, f)