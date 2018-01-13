from collections import Counter
from pprint import pprint

from asq import query

from read_svg_embedding import vertex_and_edge_lists_from_svg_file


def extract_symmetry_from_svg_file(svg_filepath):
    vertices, edges = vertex_and_edge_lists_from_svg_file(svg_filepath)
    return extract_symmetry_from_vertex_and_edge_lists(vertices, edges)


def extract_symmetry_from_vertex_and_edge_lists(vertices, edges):
    """
    Args:
        vertices: A sequence of integer vertex labels which must be
            in order around a circular embedding of the graph (the
            geometric sense of rotation is unimportant).

        edges: A sequence of 2-tuples each of which represents an
            undirected edge in the graph between two integer
            vertex labels.

    Returns:
        A sequence of 2-tuples, where the two elements of each
        pair are themselves sequences of integers.

        The integer elements of the first sequence in each pair are
        sorted integer vertex labels. For a symmetric embedding, the
        cardinality of each of these sequences will be equal
        to the order of the rotational symmetry (e.g. when the
        first sequence of each pair contains 7 elements, the
        graph embedding has 7-fold symmetry).

        The integer elements of the second sequence in each pair are
        sorted offsets around the circular embedding from each of
        the vertices in the first sequence to each of their neighbours.
        For regular graphs, the cardinality of this sequence will be
        equal to the degree of the graph. (e.g. when the second
        sequence contains 10 offsets, the graph is of regular
        degree 10). The integer offsets are modulo the number of
        vertices in the graph, so are always positive, and in the
        'forwards' direction around the circular embedding.

        Each of the offsets in the second sequence of each pair
        represents an edge from each of the vertices in the first
        sequence. So for respective sequence lengths of 7 and 10,
        70 edges are described by each pair.

        The length of the outer sequence (i.e. the number of pairs)
        will be equal to the number of vertices in the graph, divided
        by the order of the rotational symmetry. (e.g. for a 56 vertex
        graph, with 7-fold rotational symmetry, a sequence of 8 pairs
        will be returned).

        Each edge will be recorded in the returned data structure twice
        to make it easier to see other symmetries and to avoid deciding
        which would be the canonical direction. (e.g. For a 56 vertex
        graph with regular degree 10, and 7-fold rotational symmetry,
        the returned structure will describe 8*10*7=560 connections
        between vertices, when in fact the graph has only 280 edges.
    """
    # Add all edges in both directions to help us find symmetries
    reversed_edges = [(b, a) for a, b in edges]
    edges.extend(reversed_edges)

    #pprint(edges)

    assert len(vertices) == 56

    offset_edges = [(from_vertex_index, (to_vertex_index - from_vertex_index) % len(vertices))
                    for from_vertex_index, to_vertex_index in edges]

    #print('*' * 10)

    pprint(offset_edges)

    #print('*' * 10)

    sorted_offset_edges = query(offset_edges).group_by(
        key_selector=lambda edge: edge[0], # from-vertex
        element_selector=lambda edge: edge[1], # to-vertex
        result_selector=lambda key, group:  (key, tuple(sorted(group)))).to_list()

    #print(sorted_offset_edges)
    #print('*' * 10)

    sorted_offsets_sets_to_sources = query(sorted_offset_edges).group_by(
        key_selector=lambda sorted_offset_group: sorted_offset_group[1],
        element_selector=lambda sorted_offset_group: sorted_offset_group[0],
        result_selector=lambda key, group: (key, tuple(sorted(group)))).to_list()

    pprint(sorted_offsets_sets_to_sources)
    print('*' * 10)

    print(len(sorted_offsets_sets_to_sources))
    print('*' * 10)

    sources_to_sorted_offsets = sorted(((q, p) for p, q in sorted_offsets_sets_to_sources), key=lambda w: w[0])

    pprint(sources_to_sorted_offsets)
    print('*' * 10)
    return sources_to_sorted_offsets



def analyze_offset_frequencies(sources_to_sorted_offset_sets):
    c = Counter()
    for sources, offsets in sources_to_sorted_offset_sets:
        c.update(offsets)
    offset_frequencies = [c[i] for i in range(1, 56)]
    print(offset_frequencies)
    print(offset_frequencies == offset_frequencies[::-1])


if __name__ == '__main__':
    analyze_symmetry("/Users/rjs/dev/g560/embeddings/Gewirtz_graph_embeddings_3.svg")