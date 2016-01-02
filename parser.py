import cPickle as pickle
import re
from collections import defaultdict, deque

def flavor_ingredient_mapper(raw_text):
    """
    Creates a chemical compound to ingredient mapping from fenaroli's flavors. The ingredients are not individually
    extracted here, and instead returned as a single combined string
    :param raw_text: single string containing entire doc
    :return: dictionary mapping compound:ingredient list
    """

    flavor_dict = defaultdict(list)
    ignore_terms = ['EINECS No :', 'EINECS No ']
    re.MULTILINE
    ingredient_pattern = re.compile('Natural\s+occurrence:(.+)')
    compound_pattern = re.compile('(.*[A-Z]{6,20}.*)')

    blobs = raw_text.split('\n\n')
    comp_q = deque([], maxlen=3)
    ing_q = deque([], maxlen=3)
    comp_list = []
    for i in range(int(len(blobs)*0.3), int(len(blobs)*0.6)):
        text = blobs[i].replace('\n', '')
        potential_ing = re.findall(ingredient_pattern, text)
        potential_comp = re.findall(compound_pattern, text)

        if potential_comp and potential_comp[0] not in ignore_terms:
            tt1 = potential_comp[0].strip()
            comp_q.append(potential_comp[0].strip())

        if potential_ing:
            ing_q.append(potential_ing)
            try:
                new_comp = comp_q.pop()
                if new_comp in comp_q:
                    flavor_dict[comp_q[-2]] = flavor_dict[comp_q[-1]]
                else:
                    comp_q.append(new_comp)
                    flavor_dict[new_comp] = potential_ing[0].strip()
            except IndexError:
                pass

    remove_terms = ['Not reported found in nature', 'n/a', 'Reported found in nature',
                    'Data not found', 'Reported not found in nature', 'No data found ']
    flav_comp_dict = {k: v for k, v in flavor_dict.iteritems() if v not in remove_terms}
    return comp_list, flav_comp_dict

if __name__ == '__main__':
    with open('../../data/doc_joined.pkl', 'r') as f:
        joined = pickle.load(f)

    cleaned_joined = joined.replace('.', ' ')
    fcd = flavor_ingredient_mapper(cleaned_joined)