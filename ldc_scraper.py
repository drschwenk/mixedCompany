from bs4 import BeautifulSoup
import requests
from base_scraper import Scraper


class LdcScraper(Scraper):
    """
    implements methods particular to scraping of liquor.com
    """
    def __init__(self):
        super(LdcScraper, self).__init__('ldc')

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
            return returned_soup.find_all('a')

        def parse_page(search_result):
            """
            parses page returned from get request, finds links to individual drink recipes
            :param search_result: all 'a' tags from bs4 parsed html
            :return: link to a particular drink recipe as a string
            """
            links = []
            for i in search_result:
                if '/recipes/' in i['href'] and 'http' in i['href']:
                    links.append(i['href'])
            return links

        url_first = 'http://liquor.com/?post_type=recipe&s='
        url_rest_1 = 'http://liquor.com/page/'
        url_rest_2 = '/?post_type=recipe&s#038;s'

        self.drink_links += parse_page(make_request(url_first))
        for n in range(2, n_results):
            url = url_rest_1 + str(n) + url_rest_2
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
        ingredients = soup.findAll("meta", {'name':'other.ingredients'})[0].prettify().split('"')[1].split(',')
        ingredients = [i.strip()for i in ingredients]
        drink_base = soup.findAll("meta", {'name':'sailthru.base'})[0].prettify().split()[1].split('"')[1]
        ingredients.append(drink_base)
        drink_name = soup.findAll("meta", {'property':'og:title'})[0].prettify().split('"')[1]
        self.recipes[drink_name] = ingredients
        return None
