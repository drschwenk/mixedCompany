from IngredientMatcher import IngredientMatcher
from recipe_weights import compute_single_avg_weight
import random
import re

class FlavorRecommender(object):
    """
    recommends a new ingredient based on the flavor network
    """
    def __init__(self, comp_ing_dict, edge_dict, all_recipes, match_dict=None):
        """
        initializes recommender
        :param comp_ing_dict: compound : ingredient dict
        :param edge_dict: flavor network edges
        :param all_recipes: recipe dict
        :param make_match_dict: bool for building match lookup (for performance)
        :return:
        """
        self.ing_matcher = IngredientMatcher(comp_ing_dict)
        self.comp_ing_dict = self.ing_matcher.sanitized_comp_ing_dict
        cocktail_ing_lists = all_recipes.values()
        self.uniq_ing_list = list(set([i.strip().lower() for sublist in cocktail_ing_lists for i in sublist if i]))
        self.edge_dict = edge_dict
        if not match_dict:
            self.match_dict = self.ing_matcher.make_match_dict(self.uniq_ing_list)
        else:
            self.match_dict = match_dict
        self.recipe_splitter = re.compile(',\s')

    def make_rec(self, drink_recipe, flavor_threshold):
        """
        makes a single recommendation
        :param drink_recipe: user supplied recipe
        :flavor_threshold min number of shared compounds to consider
        :return: suggested ingredient
        """
        recipe_ing_list = self.recipe_splitter.split(drink_recipe)
        potential_suggestions = []
        for ingredient in self.uniq_ing_list:
            for recipe_ingredient in recipe_ing_list:
                pair = (ingredient, recipe_ingredient)
                try:
                    score = compute_single_avg_weight(pair, self.edge_dict, self.match_dict)
                    if score > flavor_threshold and pair[0] != pair[1]:
                        potential_suggestions.append(pair)
                except KeyError:
                    pass
        if potential_suggestions:
            return random.sample(potential_suggestions, min(len(potential_suggestions), 4))
        else:
            return 'no suggestion'

    def order_ingredients(suggestions, n_suggestions):
        """
        assures suggested ingredients are in the form suggestion : original ingredient,
        only needed for alternative suggestion methods (not used here)
        :param suggestions: all possible suggestions
        :param n_suggestions number of suggestions to return
        :return: suggestions in the proper order
        """
        ordered_suggestions = []
        for ipair in suggestions:
            if ipair[0] in drink_recipe:
                ordered_suggestions.append((ipair[1], ipair[0]))
            else:
                ordered_suggestions.append(ipair)
        return ordered_suggestions