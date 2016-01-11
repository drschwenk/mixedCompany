import pickle


class Scraper(object):

    def __init__(self, website):
        self.website = website
        self.drink_links = []
        self.recipes = {}

    def get_recipe_links(self, n_results):
        pass

    def get_recipe(self):
        pass

    def get_all_recipes(self):
        for drink in self.drink_links:
            self.get_recipe(drink)

    def pickle_recipes(self):
        with open('recipes.pkl', 'w') as f:
            pickle.dump(recipe_list,f )