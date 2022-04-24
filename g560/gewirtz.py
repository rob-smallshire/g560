"""The Gewirtz Graph.

An integral graph on 56 vertices and 280 egdes that is a regular graph of order 10.

This is constructed using the algorithm described in the Wolfram Mathworld page:

    http://mathworld.wolfram.com/GewirtzGraph.html
"""
import numpy
import networkx

words = (
    'abcilu', 'abdfrs', 'abejop', 'abgmnq', 'acdghp', 'acfjnt', 'ackmos',
    'ademtu', 'adjklq', 'aefgik', 'aehlns', 'afhoqu', 'aglort', 'ahijmr',
    'aipqst', 'aknpru', 'bcdekn', 'bchjqs', 'bcmprt', 'bdgijt', 'bdhlmo',
    'beflqt', 'beghru', 'bfhinp', 'bfjkmu', 'bgklps', 'bikoqr', 'bnostu',
    'cdfimq', 'cdjoru', 'cefpsu', 'cegjlm', 'cehiot', 'cfhklr', 'cginrs',
    'cgkqtu', 'clnopq', 'degoqs', 'deilpr', 'dfglnu', 'dfkopt', 'dhiksu',
    'dhnqrt', 'djmnps', 'efmnor', 'ehkmpq', 'eijnqu', 'ejkrst', 'fghmst',
    'fgjpqr', 'fijlos', 'ghjkno', 'gimopu', 'hjlptu', 'iklmnt', 'lmqrsu',
)

word_sets = tuple(map(set, words))

adjacency_matrix = [[a.isdisjoint(b) for a in word_sets] for b in word_sets]

adjacency_array = numpy.array(adjacency_matrix)

G = networkx.from_numpy_matrix(adjacency_array)

def make():
    return G.copy()
