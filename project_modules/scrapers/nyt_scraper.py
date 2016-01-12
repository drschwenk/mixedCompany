from bs4 import BeautifulSoup
import requests
from base_scraper import Scraper


class NytScraper(Scraper):
    """
    Implements methods particular to scraping of cooking.nytimes.com
    """
    def __init__(self):
        super(NytScraper, self).__init__('ldc')

    def get_recipe_links(self, n_results=124):
        """
        builds a list of links to drink recipes
        :param n_results: number of pages of search results to use
        :return: None
        """
        def make_request(search_url):
            """
            makes a single get request for a page of recipe links
            :param search_url: search url
            :return: all possible recipe links
            """
            r = requests.get(search_url)
            returned_soup = BeautifulSoup(r._content, 'html.parser')
            return returned_soup.find_all("article", {"class":"card recipe-card collection-droppable "})

        def parse_page(search_result):
            """
            parses page returned from get request, finds links to individual drink recipes
            :param search_result: all 'a' tags from bs4 parsed html
            :return: link to a particular drink recipe as a string
            """
            base_url = 'http://cooking.nytimes.com/'
            links = []
            for i in search_result:
                links.append(base_url + i['data-url'])
            return links

        url_base = 'http://cooking.nytimes.com/search?filters[dish_types][]=cocktails&q=&page='
        for n in range(1, n_results):
            url = url_base + str(n)
            results = make_request(url)
            self.drink_links += parse_page(results)
        return None

    def get_recipe(self, url):
        """
        get ingredients for a particular drink recipe
        adds ingredients to recipe dict
        :param url: link to recipe page
        :return: None
        """
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        ingredients = soup.find_all("span", {"itemprop":"name"})
        #avoid the last element, it's not an ingrdient
        ingredients = [i.prettify().split('\n')[1].strip() for i in ingredients[:-1]]
        drink_name = soup.findAll("h1", {'class':'recipe-title title name'})[0]['data-name']
        self.recipes[drink_name] = ingredients
        return None
