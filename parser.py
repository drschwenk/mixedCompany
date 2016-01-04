import cPickle as pickle
import re
from collections import defaultdict, deque


def text_from_pdf(raw_text):
    """
    Creates a chemical compound to ingredient mapping from fenaroli's flavors. The ingredients are not individually
    extracted here, and instead are returned as a single combined string
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


def make_ingredient_compound_dict(raw_text_dict):
    """
    Extracts a list of ingredients for a compound from the raw text parsed from the pdf.
    Inverts this dict to create the desired mapping of ingredients to their component flavor compounds.
    :param raw_text_dict: dict mapping flavors to raw text describing their natural occurrences.
    :return: ingredient : flavour compound dict
    """
    def ingredient_extractor(raw_ing_string):
        """
        creates ingredient list for a single compound
        :param raw_ing_string: ingredient string for a single flavor compound
        :return: extracted list of ingredients
        """
        split_seq = ['reported found in\s*', 'also reported found in', '  ', ' and ', ',',
                     ';', 'also ', 'in the oils* of', 'in\s+']
        ingr_list = [raw_ing_string.lower()]
        for term in split_seq:
            nested_list = map(lambda x: re.split(term, x), ingr_list)
            ingr_list = [i.strip() for sublist in nested_list for i in sublist if i]
        return ingr_list

    flavor_raw_text_dict = raw_text_dict.copy()
    for compound, ingr_str in flavor_raw_text_dict.iteritems():
        flavor_raw_text_dict[compound] = ingredient_extractor(ingr_str)

    ingredient_compound_dict = defaultdict(list)
    for k, v in flavor_raw_text_dict.iteritems():
        for ing in v:
            ingredient_compound_dict[ing].append(k)

    return flavor_raw_text_dict

if __name__ == '__main__':
    with open('../../data/doc_joined.pkl', 'r') as f:
        joined = pickle.load(f)
    cleaned_joined = joined.replace('.', ' ')
    fcd = make_ingredient_compound_dict(cleaned_joined)