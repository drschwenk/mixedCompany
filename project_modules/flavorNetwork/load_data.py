import cPickle as pickle


def load_data(data_dir):
    """
    loads data needed for the recommender system
    :param data_dir: path to data
    :return: recipes, flav:ing map, edges of the network backbone, precomputed string matches
    """
    file_name = 'all_recipes.pkl'
    with open (data_dir + file_name, 'r') as f:
        all_recipes = pickle.load(f)

    file_name = 'ing_flav_dict.pkl'
    with open(data_dir + file_name, 'r') as f:
        comp_ing_dict = pickle.load(f)

    file_name = 'backbone_edges_dict.pkl'
    with open(data_dir + file_name) as f:
        edge_dict = pickle.load(f)

    file_name = 'match_dict.pkl'
    with open(data_dir + file_name, 'r') as f:
        pre_match_dict = pickle.load(f)

    return comp_ing_dict, edge_dict, all_recipes, pre_match_dict