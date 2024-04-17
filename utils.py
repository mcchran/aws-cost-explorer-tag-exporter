import itertools

def dict_product(d):
    combinations = list(itertools.product(*d.values()))
    result = []
    for combination in combinations:
        result.append(dict(zip(d.keys(), combination)))
    return result


def dict_orthogonal_product(d):
    res = []
    p = {k: "" for k in d}
    for k in d:
        for v in d[k]:
            l = p.copy()
            l[k] = v
            res.append(l)
    return res


class DefaultLogger:

    @staticmethod
    def info(message):
        print(message)
        
    @staticmethod
    def debug(message):
        print(message)
        
    @staticmethod
    def error(message):
        print(message)
    
    @staticmethod
    def warning(message):
        print(message)