import unittest2 as unittest
from parser import flavor_ingredient_mapper
import cPickle as pickle

with open('../../data/doc_joined.pkl', 'r') as f:
    joined = pickle.load(f)

cleaned_joined = joined.replace('.', ' ')

class pdf_parser_test(unittest.TestCase):
    result = flavor_ingredient_mapper(cleaned_joined)

    def test_compound_1(self):
            ing_string = 'Reported found in the distillation waters of several plants, such as Carpinus betulus; also' \
                         ' identified among the constituents of tea (leaves) oil and in citronella  Also reported found' \
                         ' in numerous foods including apple juice, apricot, banana, citrus peel oils and juices,' \
                         ' blueberry, strawberry, guava, peach, pear, melon, cabbage, kohlrabi, cucumber, lettuce, ' \
                         'leek, peas, tomato, thy-mus, butter, milk, fish, fish oil, meats, hop oil, beer, grape wines, ' \
                         'peanut oil, pecans, potato chips, soybeans, avocado, olive, passion fruit, plum, Malay apple, ' \
                         'star fruit, mango, cauliflower, fig, artichoke, coriander leaf, rice, radish, lovage leaf, ' \
                         'laurel, loquat, endive, nectarines, clam, quince and tobacco'
            self.assertEquals(self.result['2-HEXENAL'], ing_string)

    def test_compound_2(self):
        with self.assertRaises(KeyError):
            self.result['ALLYL HEPTANOATE']

    def test_compound_3(self):
        ing_string = 'Reported found in grapes, mango and Roman chamomile oil'
        self.assertEquals(self.result['ISOBUTYL 2-BUTENOATE'], ing_string)

    def test_compound_4(self):
        ing_string = 'Reported  found  in  apricot,  banana,  apple,  strawberry,  blue  and  Gruyere  cheeses,' \
                     '  cognac,  port  wine,  rum, honey, olive, passion fruit, plum, beans, mushrooms, mango, ' \
                     'apple brandy, quince, cherimoya, kiwifruit and Chinese quince peel'
        self.assertEquals(self.result['ISOBUTYL BUTYRATE'], ing_string)

    def test_compound_5(self):
        ing_string = 'Reported found in kumquat peel oil'
        self.assertEquals(self.result['ISOBUTYL CINNAMATE'], ing_string)

    def test_compound_6(self):
        with self.assertRaises(KeyError):
            self.result['2-ACETYL-1-PYRROLINE']

    def test_compound_7(self):
        ing_string = 'Reported found in papaya'
        self.assertEquals(self.result['TRIACETIN'], ing_string)

    def test_compound_8(self):
        ing_string = 'Reported found in apple, pear, grape, pineapple, strawberry, raspberry, tomato, black currant, ' \
                     'citrus, onion and potato; also reported found in cocoa leaves, in Mexican goosefoot and in the ' \
                     'oils of coriander and lavender  In trace amounts it has been reportedly identified in the oil ' \
                     'of bitter orange, in distilled wine and in coffee aroma'
        self.assertEquals(self.result['ACETONE'], ing_string)

if __name__ == '__main__':
    unittest.main()