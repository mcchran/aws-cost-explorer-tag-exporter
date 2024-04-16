import itertools

def get_dict_product(d):
    combinations = list(itertools.product(*d.values()))
    result = []
    for combination in combinations:
        result.append(dict(zip(d.keys(), combination)))
    return result