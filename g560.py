"""Two different algorithms for constructing the g560 graph (a.k.a. GP-graph).
"""

from collections import OrderedDict
from pprint import pprint

from networkx import Graph, union

import gewirtz
import petersen
from analyze_symmetry import extract_symmetry_from_vertex_and_edge_lists
from read_svg_embedding import vertex_and_edge_lists_from_svg_file, graph_from_vertex_and_edge_lists


def make(g=None, p=None):
    """Construct a g560 graph (a.k.a. GP-graph) using the supplied Gewirtz and Peterson graphs.

    The separate node numbering schemes of the Gewirtz and Peterson graphs are
    preserved in the labelling scheme of the nodes in the new graph, which have
    will be strings of the form "G-P" where G and P are the respective names from
    the supplied Gewirtz and Peterson graphs.

    Args:
        g: An optional Gewirtz graph. If not supplied the default Gewirtz graph will be used.
        p: An optional Peterson graph. If not supplied the default Peterson graph will be used.

    Returns:
        A g560 graph.
    """

    g = g or gewirtz.make()
    p = p or petersen.make()

    # Make a disconnected graph containing 56 disconnected Peterson graphs

    s = Graph()

    # Add 560 nodes by adding one Petersen graph (10 nodes) for each
    # of the 56 nodes of the gewirtz graph.
    for g_node in g.nodes:
        s = union(s, p, rename=('', '{}-'.format(g_node)))

    neighbours = {n:list(g.neighbors(n)) for n in g.nodes}

    for g_edge in g.edges:
        # This edge will be the ith outedge and jth inedge
        # Connect g_edge_from-i to g_edge_to-j

        g_from_node, g_to_node = g_edge
        i = neighbours[g_from_node].index(g_to_node)
        j = neighbours[g_to_node].index(g_from_node)

        s_from_node = '{}-{}'.format(g_from_node, i)
        s_to_node = '{}-{}'.format(g_to_node, j)

        #print("{} -- {}".format(s_from_node, s_to_node))

        s.add_edge(s_from_node, s_to_node)

    return s


def make_symmetrical(gewirtz_svg_filepath="/Users/rjs/dev/g560/embeddings/Gewirtz_graph_embeddings_1.svg", p=None):
    """Make a g560 graph, respecting any symmetries in the specified Gewirtz graph.

    The separate node numbering schemes of the Gewirtz and Peterson graphs are
    preserved in the labelling scheme of the nodes in the new graph, which have
    will be strings of the form "G-P" where G and P are the respective names from
    the supplied Gewirtz and Peterson graphs.

    Args:
        gewirtz_svg_filepath: An SVG file containing data containing a symmetrical representation
            of the Gewirtz graph.
        p: An optional Peterson graph. If not supplied the default Peterson graph will be used.

    Returns:
        A g560 graph.
    """

    g_vertex_list, g_edge_list = vertex_and_edge_lists_from_svg_file(gewirtz_svg_filepath)

    g = graph_from_vertex_and_edge_lists(g_vertex_list, g_edge_list)
    p = p or petersen.make()

    s = Graph()

    # Add 560 nodes by adding one Petersen graph (10 nodes) for each
    # of the 56 nodes of the gewirtz graph.
    for g_node in g.nodes:
        s = union(s, p, rename=('', '{}-'.format(g_node)))

    sources_to_offsets = extract_symmetry_from_vertex_and_edge_lists(g_vertex_list, g_edge_list)

    source_to_ordered_edges = OrderedDict()
    for sources, offsets in sources_to_offsets:
        for source in sources:
            targets = [(source + offset) % len(g_vertex_list) for offset in offsets]
            source_to_ordered_edges[source] = targets
    pprint(source_to_ordered_edges)

    for g_source, g_targets in source_to_ordered_edges.items():
        for p_source, g_target in enumerate(g_targets):
            p_target = source_to_ordered_edges[g_target].index(g_source)
            s_source = '{}-{}'.format(g_source, p_source)
            s_target = '{}-{}'.format(g_target, p_target)
            print("{} -- {}".format(s_source, s_target))
            s.add_edge(s_source, s_target)

    return s

if __name__ == '__main__':
    s = make_symmetrical()
