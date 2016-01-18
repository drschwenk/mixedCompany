from fuzzywuzzy import fuzz, process
from ingredient_lookup import IngredientDecomposer


class IngredientMatcher(object):
    """
    matches cocktail recipes ingredients to their matches from the flavor handbook
    """
    def __init__(self, comp_ing_dict):
        self.decomposer = IngredientDecomposer()
        self.sanitized_comp_ing_dict = {k.decode('utf-8'): v for k, v in comp_ing_dict.iteritems()}
        self.match_dict = {}

    def make_match_dict(self, unique_ing_list):
        return {k: self.match_ingredients([k]) for k in unique_ing_list}

    def match_ingredients(self, recipe):
        """
        Makes a fuzzy match between ingredients in a recipe and in the ingredient:compound dict
        :param recipe: ingredients to match
        :param comp_ing_dict: compound ingredient dict
        :return:
        """
        matches = []
        for ing in recipe:
            component_matches = self.decomposer.get_component_ingredients(ing)
            if component_matches:
                return self.match_ingredients(component_matches)
            match_list = process.extractBests(ing, self.sanitized_comp_ing_dict.keys(),
                                              scorer=fuzz.ratio, score_cutoff=98)
            matches += [match[0] for match in match_list]
            match_list = process.extractBests(ing, self.sanitized_comp_ing_dict.keys(),
                                              scorer=fuzz.token_sort_ratio,
                                              score_cutoff=85)
            matches += [match[0] for match in match_list]
            if not matches:
                sub_ing = ing.split()
                for i in sub_ing:
                    match_list = process.extractBests(i, self.sanitized_comp_ing_dict.keys(),
                                                      scorer=fuzz.ratio, score_cutoff=88)
                    matches += [match[0] for match in match_list]
        return list(set(matches))

    def lookup_match(self, ingredient):
        return self.match_dict[ingredient]