from pprint import pprint
from statistics import mean

from euclidian.cartesian2 import Point2
from lxml import etree
from networkx import Graph


def vertex_and_edge_lists_from_svg_file(svg_filepath):
    """Read an SVG representation of a graph.

    The graph must be a circular embedding, with all nodes
    lying on a circle, and all edges as chords of the circle.

    Assumes the following SVG structure:

        <svg>
            <g>
                <g>
                    <g>
                        <line y2="3073.5" x2="1371.8" y1="2477" x1="1200"/>
                        <line y2="2547.5" x2="1401.4" y1="2477" x1="1200"/>
                        ...
                        <line y2="2628.2" x2="1473.5" y1="2800" x1="877"/>
                    </g>
                    <g>
                        <circle r="6" cy="2477" cx="1200"/>
                        <circle r="6" cy="2598.6001" cx="1452.5"/>
                        ...
                        <circle r="6" cy="2547.5" cx="998.59998"/>
                    </g>
                </g>
            </g>
        </svg>

    Where line elements are used to represent edges, and circle elements are
    used to represent vertices (nodes). Correspondence is done on the basis
    of equality of coordinates.

    Args:
        svg_filepath: An SVG file containing data with the above structure.

    Returns:
        A 2-tuple where the first element is a sequence of integer vertex labels,
        and the second is a sequence of 2-tuples representing undirected edges.
        The vertices will be ordered anticlockwise from the negative x axis.

    """
    tree = etree.parse(svg_filepath)
    root = tree.getroot()
    edge_group = root[0][0][0]
    node_group = root[0][0][1]
    return vertex_and_edge_lists_from_svg_elements(node_group, edge_group)


def vertex_and_edge_lists_from_svg_elements(node_group, edge_group):
    """Read a graph data structure from a circular embedding.

    The graph must be a circular embedding, with all nodes
    lying on a circle, and all edges as chords of the circle.

    Args:
        node_group: An SVG group element containing circle elements,
            the center points of which must coincide with the end of
            the lines in the edge_group, in order to correlate these
            nodes with those edges.

        edge_group: An SVG group element containing line elements,
            the end points of which must coincide with the centres of
            the circles in the node_group, in order to correlate these
            edges with those nodes.

    Returns:
        A 2-tuple where the first element is a sequence of integer vertex labels,
        and the second is a sequence of 2-tuples representing undirected edges.
        The vertices will be ordered anticlockwise from the negative x axis.
    """
    geometric_vertices = []
    for i, node in enumerate(node_group):
        geometric_vertices.append(Point2(x=float(node.attrib['cx']),
                                         y=float(node.attrib['cy'])))
    center = Point2(x=mean(v.x for v in geometric_vertices),
                    y=mean(v.y for v in geometric_vertices))
    geometric_vertices.sort(key=lambda v: (v - center).atan2())

    geometric_edges = []
    for edge in edge_group:
        source_vertex = Point2(x=float(edge.attrib['x1']),
                               y=float(edge.attrib['y1']))
        target_vertex = Point2(x=float(edge.attrib['x2']),
                               y=float(edge.attrib['y2']))
        edge = (source_vertex, target_vertex)
        geometric_edges.append(edge)

    vertices = range(len(geometric_vertices))
    edges = [(geometric_vertices.index(from_vertex),
              geometric_vertices.index(to_vertex))
             for from_vertex, to_vertex in geometric_edges]
    return vertices, edges


def graph_from_vertex_and_edge_lists(vertices, edges):
    graph = Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)
    return graph


def graph_from_svg_file(svg_filepath):
    return graph_from_vertex_and_edge_lists(
        *vertex_and_edge_lists_from_svg_file(svg_filepath))


