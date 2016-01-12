from fuzzywuzzy import fuzz, process
from collections import defaultdict
from itertools import permutations
import cPickle as pickle


def match_ingredients(recipe, comp_ing_dict):
    """
    Makes a fuzzy match between ingredients in a recipe and in the ingredient:compound dict
    :param recipe: ingredients to match
    :param comp_ing_dict: compound ingredient dict
    :return:
    """
    sanitized_comp_ing_dict = {k.decode('utf-8'): v for k, v in comp_ing_dict.iteritems()}
    matches = []
    for ing in recipe:
        match_list = process.extractBests(ing, sanitized_comp_ing_dict.keys(), scorer=fuzz.ratio, score_cutoff=98)
        matches += [match[0] for match in match_list]
        match_list = process.extractBests(ing, sanitized_comp_ing_dict.keys(), scorer=fuzz.partial_token_set_ratio,
                                          score_cutoff=80)
        matches += [match[0] for match in match_list]
    return list(set(matches))


def compute_single_avg_weight(recipe, comp_ing_dict, edge_dict, match_dict):
    """
    computes the average weight of the ingredients in a recipe
    :param recipe single list of ingredients
    :param comp_ing_dict compound ingredient dict
    :param edge_dict: dict of edges comprising the flavor network
    :return: avg weight of this recipe
    """
    ingredients = []
    for ing in recipe:
        if ing:
            ingredients += match_dict[ing]
    pairwise_combos = permutations(ingredients, 2)
    tot_weight = 0
    norm_factor = float(2) / (len(recipe)*(len(recipe)-1))
    # I use permutations here because there's no way to know how the ingredients are ordered in the edge dict's keys
    edge_ids = []
    for ing_pair in pairwise_combos:
        edge_ids.append(ing_pair[0] + ', ' + ing_pair[1])
    for edge_id in edge_ids:
        tot_weight += edge_dict[edge_id]
    return tot_weight * norm_factor


def compute_all_weights(recipe_dict, comp_ing_dict, edge_list):
    """
    Computes average ingredient weights for all recipes
    :param recipe_dict: dictionary of cocktail recipes
    :param comp_ing_dict: flavor component : ingredient dict
    :param edge_list: list of edges from the flavor network
    :return: dictionary of average weights
    """
    unique_ing_list = list(set([i for sublist in recipe_dict.values() for i in sublist if i]))
    print len(unique_ing_list)
    match_dict = {k:match_ingredients([k], comp_ing_dict) for k in unique_ing_list}
    recipe_weights = defaultdict(float)
    for recipe_name, ingredients in recipe_dict.iteritems():
        recipe_weights[recipe_name] = compute_single_avg_weight(ingredients, comp_ing_dict, edge_list, match_dict)
    return recipe_weights

if __name__ == '__main__':
    with open('./data/backbone_edges_dict.pkl') as f:
        edge_dict = pickle.load(f)
    with open('./data/second_ing_flav_dict.pkl', 'r') as f:
        comp_ing_dict = pickle.load(f)
    with open('./data/comb_recipes.pkl', 'r') as f:
        comb_recipes = pickle.load(f)
    weight_dict = compute_all_weights(comb_recipes, comp_ing_dict, edge_dict)
    with open('./new_avg_recipe_weights.pkl', 'w') as f:
        pickle.dump(weight_dict, f)