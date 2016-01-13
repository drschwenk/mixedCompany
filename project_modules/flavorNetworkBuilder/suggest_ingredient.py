
def ingred_opt(drink_recipe):
    max_score = ('max_ingrd', 0)
    for ingredient in cocktail_set_list:
        score = 0
        pairings = permutations(drink_recipe + [ingredient], 2)
        for pair in pairings:
            try:
                score += compute_single_avg_weight(pair, comp_ing_dict, edge_dict, match_dict)
            except KeyError:
                pass
        if score > max_score[1]:
            max_score = (ingredient, score)
    return max_score