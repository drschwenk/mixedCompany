import pickle


class Scraper(object):
    """
    Base class for cocktail recipe scraping
    """
    def __init__(self, website):
        """
        drink_links will contain urls of single drink recipes
        recipes are stored as drink name : ingredient list
        :param website: website to scrape and parse
        :return:
        """
        self.website = website
        self.drink_links = []
        self.recipes = {}

    def get_recipe_links(self, n_results):
        pass

    def get_recipe(self, url):
        pass

    def get_all_recipes(self):
        """
        gets recipes for all links in the drinks list
        :return: None
        """
        for drink in self.drink_links:
            self.get_recipe(drink)
        return None

    def pickle_recipes(self):
        """
        writes recipe dict to pickle file
        :return:
        """
        with open('recipes.pkl', 'w') as f:
            pickle.dump(self.recipes, f)
        return None