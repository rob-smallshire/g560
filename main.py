import code
import sys
from collections import Counter

from networkx import diameter, radius, eccentricity, adjacency_spectrum, average_shortest_path_length, adjacency_matrix

from g560 import make, make_symmetrical


def main():
    """Interrograte the g560 graph.
    """
    g560 = make_symmetrical()
    print("g560 (a.k.a GP-graph)")
    print("=====================")
    print()
    print("Number of nodes :", len(g560))
    print("Number of edges :", len(g560.edges))
    print("Diameter        :", diameter(g560))
    print("Radius          :", radius(g560))
    print("Average shortest path length :", average_shortest_path_length(g560))

    #code.interact(local=locals())

    eccentricities = Counter(eccentricity(g560).values())

    print("Eccentricities")
    for e in sorted(eccentricities):
        print("  {} for {} nodes".format(e, eccentricities[e]))

    print("Adjacency spectrum :", adjacency_spectrum(g560))

    text_matrix = '\n'.join(''.join(" X"[g560.has_edge(u, v)] for v in g560.nodes) for u in g560.nodes)

    print(text_matrix)

    return 0

if __name__ == '__main__':
    sys.exit(main())
