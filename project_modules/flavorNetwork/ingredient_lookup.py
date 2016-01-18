class IngredientDecomposer(object):
    """
    lookup table breaking down common cocktail ingredients into their components
    """
    def __init__(self):
        self.ingredient_lookup = {
            'angostura bitters': [
                                    'dried orange peel',
                                    'sour cherries',
                                    'cinnamon sticks',
                                    'vanilla bean'
                                    'cloves',
                                    'quassia chips',
                                    'juniper berries',
                                    'cocoa nibs',
                                    'black walnut leaf',
                                    'cassia',
                                    'wild cherry bark',
                                    'orris root'
                                 ],
            'campari': [
                'bitter orange peel',
                'Angelica Root',
                'Buckbean Leaves',
                'lemon peel',
                'Anise',
                'Calamus',
                'Fennel',
                'Orris Root',
                'wormwood',
                'Cinnamon',
                'Cloves',
                'Marjoram',
                'Sage',
                'Thyme',
                'Rosemary'
            ],
            'aperol': [
                    'bitter orange',
                    'gentian',
                    'rhubarb',
                    'cinchona'
                ],
            'lillet': [
                'wine',
                'sweet oranges',
                'bitter oranges'
            ],
            'gran classico bitter': [
                'wormwood',
                'gentian',
                'bitter oranges',
                'rhubarb',
                'hyssop'
            ],
            'jagermeister': [
                'citrus peel',
                'licorice',
                'anise',
                'poppy seeds',
                'saffron',
                'ginger',
                'juniper berries',
                'ginseng'
            ],
            'grand mariner': [
                'cognac',
                'bitter orange',
                'sugar'
            ],
            'kahlua': [
                'coffee',
                'vanilla beans',
                'rum',
                'corn syrup'
            ],
            'limoncello': [
                'lemon zest',
                'simple syrup'
            ],
            'cointreau': [
                'sweet orange',
                'bitter orange'
            ],
            'triple sec': [
                'sweet orange',
                'bitter orange'
            ],
            'curacao': [
                'bitter orange'
            ],
            'st. germain': [
                'elderflower'
            ],
            'ouzo': [
                'anise'
            ],
            'grenadine': [
                'blackcurrant'
            ],
            'benedictine': [
                'angelica',
                'hyssop',
                'lemon balm'
            ],
            'applejack': [
                'apples'
            ],
            'creme de noyaux': [
                'apricot kernels'
            ],
            'kummel': [
                'caraway seeds',
                'cumin',
                'fennel'
            ]
        }

    def get_component_ingredients(self, compound_ingredient):
        try:
            return self.ingredient_lookup[compound_ingredient]
        except KeyError:
            return None
