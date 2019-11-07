from itertools import starmap, repeat
from functools import reduce, partial
import dill as pickle
from toolz.sandbox.parallel import fold
from pathos.multiprocessing import ProcessingPool as PathosPool
from multiprocessing import Pool
from csv import DictReader

def unique_keys(left, right):
    return set(left.keys()).union(set(right.keys()))

def prod(xs):
    return reduce(lambda acc,nxt: acc*nxt, xs)

def compute_prob(model, k, v, label, N):
    Cn = model['LABELS'][label]
    prior = Cn / N
    evidence = model[k][v].get(label,.001) / Cn
    return prior * evidence

def _nb_suggest(ob, model, target):
    ob.pop(target)
    N = sum(model['LABELS'].values())
    results = {}
    for label in model['LABELS'].keys():
        p = prod(compute_prob(model, k, v, label, N) for k, v in ob.items())
        results[label] = p
    return results

def naive_bayes_suggest(obs, model, target):
    with Pool() as P:
        f = partial(_nb_suggest, target=target)
        return P.starmap(f, zip(obs, repeat(model)))

def nb_acc(acc, nxt, target):
    label = nxt.pop(target)
    if not acc.get('LABELS', False):
        acc['LABELS'] = {}
    acc['LABELS'][label] = acc['LABELS'].get(label,0) + 1
    for k,v in nxt.items():
        if not acc.get(k,False):
            acc[k] = {}
        if not acc[k].get(v, False):
            acc[k][v] = {}
        acc[k][v][label] = acc.get(k,{}).get(v,{}).get(label,0) + 1
    return acc

def _nb_comb(left, right):
    acc = {}
    acc['LABELS'] = {}
    for k in unique_keys(left['LABELS'], right['LABELS']):
        acc['LABELS'][k] = left['LABELS'].get(k,0) + right['LABELS'].get(k,0)
    for k in unique_keys(left, right):
        if k == 'LABELS': continue
        acc[k] = {}
        for v in unique_keys(left.get(k,{}), right.get(k,{})):
            acc[k][v] = {}
            for label in acc['LABELS']:
                count_left = left.get(k,{}).get(v,{}).get(label,0)
                count_right = right.get(k,{}).get(v,{}).get(label,0)
                acc[k][v][label] = count_left + count_right
    return acc

def naive_bayes(xs, target):
    acc = partial(nb_acc, target=target)
    with PathosPool() as P:
        model = fold(acc, xs, {}, map=P.map, combine=_nb_comb)
    return partial(naive_bayes_suggest, model=model, target=target)

def max_prob(probs):
    return max(((k,v) for k,v in probs.items()), key=lambda x:x[1])[0]

if __name__ == "__main__":
    # Download the nursery data and assign its path to fp
    # https://archive.ics.uci.edu/ml/machine-learning-databases/nursery/nursery.data
    fp = "/home/jt-w/Downloads/nursery.data"
    with open(fp) as f:
        reader = DictReader(f, fieldnames=["parents", "has_nurs", "form",
                                     "children", "housing", "finance",
                                     "social", "health", "recc"])
        data = [row for row in reader]

    model = naive_bayes(data, "recc")
    probs = model(data)
    print("{}\t\t{}\t{}".format("Match", "Suggestion", "Actual"))
    print("{}".format("-"*45))
    for i,p in enumerate(probs):
        suggestion = max_prob(p)
        actual = data[i]['recc']
        match = suggestion == actual
        print("{}\t\t{}\t{}".format(match, suggestion, actual))
        if i > 25: break
