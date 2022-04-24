import networkx
from networkx.generators.small import make_small_undirected_graph

# A Petersen graph where the vertex order is a Hamiltonian path
description = [
    "adjacencylist",
    "Petersen Graph",
    10,
    [
        [2, 5, 8],  # 1
        [1, 3, 10], # 2
        [2, 4, 7],  # 3
        [3, 5, 9],  # 4
        [4, 6, 1],  # 5
        [5, 7, 10], # 6
        [6, 8, 3],  # 7
        [7, 9, 1],  # 8
        [8, 10, 4], # 9
        [9, 2, 6],  # 10
    ]
]
P = make_small_undirected_graph(description)
assert len(P) == 10
assert len(P.edges) == 15
assert all(d == 3 for _, d in P.degree)

#P = networkx.petersen_graph()

def make():
    return P.copy()
