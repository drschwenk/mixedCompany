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
    ignore_terms = ['EINECS No :', 'EINECS No ']
    # These must be removed here to preserve the queue ordering
    ingredient_pattern = re.compile('Natural\s+occurrence:(.+)')
    compound_pattern = re.compile('(.*[A-Z]{6,20}.*)')
    blobs = raw_text.split('\n\n')

    flavor_dict = defaultdict(list)
    comp_q = deque([], maxlen=3)
    ing_q = deque([], maxlen=2)
    for blob in blobs:
        text = blob.replace('\n', '')
        potential_ing = re.findall(ingredient_pattern, text)
        potential_comp = re.findall(compound_pattern, text)

        if potential_comp and potential_comp[0] not in ignore_terms:
            comp_q.append(potential_comp[0].strip())
        if potential_ing:
            ing_q.append(potential_ing[0].strip())
            try:
                c1 = comp_q[0]
                c2 = comp_q[1]
                c3 = comp_q[2]
                # This is to check for page headers in the compound queue
                if c2 == c1:
                    flavor_dict[c2] = ing_q[-1]
                else:
                    flavor_dict[c3] = ing_q[-1]
            except IndexError:
                pass
    # Removing the compounds not found in nature
    remove_terms = ['Not reported found in nature', 'n/a', 'Reported found in nature',
                    'Data not found', 'Reported not found in nature', 'No data found ']
    flav_comp_dict = {k: v for k, v in flavor_dict.iteritems() if v not in remove_terms}
    return flav_comp_dict

if __name__ == '__main__':
    with open('../../data/doc_joined.pkl', 'r') as f:
        joined = pickle.load(f)
    cleaned_joined = joined.replace('.', ' ')
    fcd = flavor_ingredient_mapper(cleaned_joined)