from itertools import combinations

import networkx

from g560 import gewirtz


def symmetric_difference(graph, cycle_a, cycle_b):
    # get edges
    edges_a = list(graph.subgraph(cycle_a).edges())
    edges_b = list(graph.subgraph(cycle_b).edges())

    # also get reverse edges as graph undirected
    edges_a += [e[::-1] for e in edges_a]
    edges_b += [e[::-1] for e in edges_b]

    # find edges that are in either but not in both
    edges_c = set(edges_a) ^ set(edges_b)

    cycle_c = frozenset(networkx.Graph(list(edges_c)).nodes())
    return cycle_c

def cycles(g):
    cycle_basis = networkx.cycle_basis(g)
    for cycle_a, cycle_b in combinations(cycle_basis, 2):
        yield symmetric_difference(g, cycle_a, cycle_b)
    yield from map(frozenset, cycle_basis)

def main():
    g = gewirtz.make()
    cs = cycles(g)
    quads = [tuple(c) for c in cs if len(c) == 4]
    print(quads)
    print(len(quads))
    freq = sorted((sum(1 for q in quads if i in q) for i in range(56)))
    print(freq)

if __name__ == '__main__':
    main()
