from collections import Counter
from itertools import combinations, chain
from pprint import pprint

from asq import query

from g560 import gewirtz


def find_quads(g):
    for a in g.nodes:
        sa = {a}
        for b, c in combinations(g.neighbors(a), 2):
            sb = set(g.neighbors(b)) - sa
            sc = set(g.neighbors(c)) - sa
            for d in sb.intersection(sc):
                yield (a, b, d, c)



def main():
    g = gewirtz.make()
    q = list(find_quads(g))
    print(len(q))

    quads = query(q).distinct(frozenset).to_list()

    # https://books.google.no/books?id=brziBQAAQBAJ&pg=PA123&lpg=PA123&dq=gewirtz+630&source=bl&ots=GoniUSAlUk&sig=Fq_7YVjAprOPofYs3_Kvn1wUjKY&hl=no&sa=X&ved=0ahUKEwj96v24ov7ZAhWGJJoKHZ3FAOAQ6AEILjAB#v=onepage&q=gewirtz%20630&f=false
    assert len(quads) == 630

    pprint(quads)

    shorts, longs = list(zip(*(((a, b, c), (a, d, c)) for a, b, c, d in quads)))

    counter = Counter(x for triplet in chain(shorts, longs) for x in triplet if triplet[1] == 37)
    print(counter)



if __name__ == '__main__':
    main()