import cPickle as pickle
import re
from collections import defaultdict, deque

def flavor_ingredient_mapper(raw_text, look_ahead_range):
    """
    Creates a chemical compound to ingredient mapping from fenaroli's flavors. The ingredients are not individually
    extracted here, and instead returned as a single combined string
    :param raw_text: single string containing entire doc
    :return: dictionary mapping compound:ingredient list
    """

    def check_for_header(new_comp, text_blobs, look_ahead_index, target_pattern):
        """
        Searches for compound appearing in a header, which would produce a duplicate entry if not caught
        :param new_comp: compound being evaluated
        :param text_blobs:
        :param look_ahead_index:
        :param target_pattern:
        :return:
        """
        for j in range(look_ahead_index, look_ahead_index + look_ahead_range):
            try:
                r1 = re.findall(target_pattern, text_blobs[j])
                if new_comp == re.findall(target_pattern, text_blobs[j]):
                    # a potential match has been found
                    return True
            except KeyError:
                pass
        return False

    flavor_dict = defaultdict(list)
    ignore_terms = ['EINECS No :']
    re.MULTILINE
    ingredient_pattern = re.compile('Natural occurrence:(.+)')
    compound_pattern = re.compile('(.*[A-Z]{6,20}.*)')

    blobs = raw_text.split('\n\n')
    comp_q = deque([], maxlen=3)
    for i in range(int(len(blobs)*0.2), len(blobs)):
        text = blobs[i].replace('\n', '')
        ing = re.findall(ingredient_pattern, text)
        comp = re.findall(compound_pattern, text)
        if comp and comp[0] not in ignore_terms:
            if not check_for_header(comp, blobs, i, compound_pattern):
                comp_q.append(comp[0])
        if ing:
            try:
                flavor_dict[comp_q.pop().strip()] = ing[0].strip()
            except IndexError:
                pass

    remove_terms = ['Not reported found in nature','n/a','Reported found in nature',
                    'Data not found', 'Reported not found in nature', 'No data found ']
    flav_comp_dict = {k:v for k,v in flavor_dict.iteritems() if v not in remove_terms}
    return flav_comp_dict


with open('../../data/doc_joined.pkl', 'r') as f:
    joined = pickle.load(f)

cleaned_joined = joined.replace('.', ' ')
fcd = flavor_ingredient_mapper(cleaned_joined, 50)

print(fcd['2-HEXENAL'])