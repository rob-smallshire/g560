from itertools import permutations

from networkx import Graph, union, average_shortest_path_length

from g560 import petersen
from g560.analyze_symmetry import extract_symmetry_from_vertex_and_edge_lists
from g560.read_svg_embedding import vertex_and_edge_lists_from_svg_file, graph_from_vertex_and_edge_lists


def find_optimal_permutations_for_node(gewirtz_svg_filepath, p=None):
    g_vertex_list, g_edge_list = vertex_and_edge_lists_from_svg_file(gewirtz_svg_filepath)

    g = graph_from_vertex_and_edge_lists(g_vertex_list, g_edge_list)
    p = p or petersen.make()

    sources_to_offsets = extract_symmetry_from_vertex_and_edge_lists(g_vertex_list, g_edge_list)

    for sources, offsets in sources_to_offsets:
        s = Graph()
        g_node = sources[0]  # We only need the first - the others are the same, by symmetry

        for g_edge in g.edges:
            if g_node not in g_edge:
                s.add_edge(*g_edge)

        s = union(s, p, rename=('', '{}-'.format(g_node)))

        assert len(s) == 65

        print(s.nodes)

        targets = [str((g_node + offset) % len(g_vertex_list)) for offset in offsets]

        print("source = {}, targets = {}".format(g_node, targets))

        min_aspl = float("+inf")
        t = s.copy()     # We add and remove edges from a single copy of the graph
        gp_edges = []    # rather than making a new graph every time for performance reasons
        for i, target_g_nodes in enumerate(permutations(targets)):
            #print(target_g_nodes)

            assert len(p.nodes) == len(target_g_nodes)

            gp_edges.clear()
            for p_node, target_g_node in zip(p.nodes, target_g_nodes):
                tp_node = '{}-{}'.format(g_node, p_node)
                #print(tp_node, target_g_node)
                gp_edges.append((tp_node, target_g_node))
                #t.add_edge(tp_node, target_g_node)
            #print(len(t))

            t.add_edges_from(gp_edges)

            #assert len(t) == 65
            #assert len(t.edges) == 295

            # TODO: Remember which permuation improved the ASPL!
            aspl = average_shortest_path_length(t)
            if aspl < min_aspl:
                print("New minimum ASPL: {aspl} for permutation {i} which is {target_g_nodes}".format(
                    aspl=aspl, i=i, target_g_nodes=target_g_nodes))
                min_aspl = aspl

            t.remove_edges_from(gp_edges)
            #assert len(t) == 65
            #assert len(t.edges) == 285


if __name__ == '__main__':
    find_optimal_permutations_for_node("/Users/rjs/dev/g560/embeddings/Gewirtz_graph_embeddings_1.svg")