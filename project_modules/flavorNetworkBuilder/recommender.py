from IngredientMatcher import IngredientMatcher
from recipe_weights import compute_single_avg_weight
from itertools import permutations
import random

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

    def make_rec(self, drink_recipe):
        """
        makes a single recommendation
        :param drink_recipe: user supplied recipe
        :return: suggested ingredient
        """

        # def filter_common(ing, score):
        #     thresholds = {
        #         'kahlua': 4000,
        #         'nonalcoholic apple cider or juice': 4000,
        #         'mango rum': 2000,
        #         'sweet apple cider': 3000,
        #         'apple cider syrup': 3000,
        #         'sparkling apple cider': 3000,
        #         'fresh apple cider': 3000,
        #         'apple cider': 3000,
        #         'apple butter': 3000,
        #         'coffee beans': 3000
        #
        #     }
        #     try:
        #         return thresholds[ing] < score
        #     except KeyError:
        #         return True

        max_score = ('no suggestion', 0)
        for ingredient in self.uniq_ing_list:
            score = 0
            pairings = permutations(drink_recipe + [ingredient], 2)
            for pair in pairings:
                try:
                    score += compute_single_avg_weight(pair, self.edge_dict, self.match_dict)
                except KeyError:
                    pass
            if score > max_score[1]:
                max_score = (ingredient, score)
        return max_score

    def make_rec_2(self, drink_recipe):
        """
        makes a single recommendation
        :param drink_recipe: user supplied recipe
        :return: suggested ingredient
        """

        max_score = ('no suggestion', 0)
        potential_suggestions = []
        for ingredient in self.uniq_ing_list:
            score = 0
            pairings = permutations(drink_recipe + [ingredient], 2)
            for pair in pairings:
                try:
                    score, norm = compute_single_avg_weight(pair, self.edge_dict, self.match_dict)
                    if score > 10:
                        potential_suggestions.append(ingredient)
                    if score/float(norm+1) > max_score[1]:
                        max_score = (ingredient, score)
                except KeyError:
                    pass
        return random.choice(potential_suggestions)

