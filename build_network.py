from graphlab import SGraph, Vertex, Edge
import cPickle as pickle
from math import sqrt


def build_weighted_graph(ing_comp_dict):
    """
    Builds the weighted, undirected graph that is the flavor network
    :param ing_comp_dict: ingredient:compound dictionary
    :return: SGraph that represents the flavor network
    """
    flavor_network = SGraph()
    vertices = []
    edge_list = []
    ingredients = ing_comp_dict.keys()

    for ingredient_node_1, compounds in ing_comp_dict.iteritems():
        ingredients.remove(ingredient_node_1)
        vertices.append(Vertex(ingredient_node_1, attr={'deg': 0}))
        for ingredient_node_2 in ingredients:
            weight = len(set(ing_comp_dict[ingredient_node_2]).intersection(set(compounds)))
            if weight > 0:
                edge_list.append(Edge(ingredient_node_1, ingredient_node_2, attr={'weight': weight}))
        vertices.append(Vertex(ingredient_node_1))

    flavor_network = flavor_network.add_vertices(vertices)
    flavor_network = flavor_network.add_edges(edge_list)
    return flavor_network, vertices, edge_list


def extract_backbone(flavor_network, vertices, edges, alpha):
    """
    Builds a new graph with only the edges with weights that exceed the threshold for statistical significance
    :param flavor_network: flavor-ingredient network to prune
    :param vertices: separate list of vertices (to speed extraction)
    :param edges: separate list of edges (to speed extraction)
    :param alpha: threshold p-value for keeping an edge in the network
    :return: the pruned SGraph
    """
    def degree_count_fn(src, connecting_edge, dst):
        """
        increments the degree of the nodes on this edge
        :param src: source node
        :param connecting_edge: connecting edge
        :param dst: destination node
        :return: source and destination with degree attribute incremented
        """
        src['deg'] += 1
        dst['deg'] += 1
        return src, connecting_edge, dst

    def compute_node_moments(node_k):
        """
        computes mean and standard deviation for this node
        :param node_k: node to compute
        :return: mean and sigma
        """
        mean = 2*node_k/(node_k+1)
        sigma = sqrt(node_k**2*((20 + 4*node_k)/((node_k + 1)*(node_k + 2)*(node_k + 3)) - 4/(node_k + 1)**2))
        return mean, sigma

    def test_for_significance(edge, weights_lookup, alpha):
        """
        tests this edge for statistical significance based on it's source and destination nodes
        :param edge: edge to test
        :param weights_lookup: quick (hash table) lookup for the edge weights
        :param alpha: significance threshold
        :return: significance boolean check
        """
        y_obs = edge.attr['weight']
        node1_k = weights_lookup[edge.dst_vid]
        node2_k = weights_lookup[edge.src_vid]
        m1, sig1 = compute_node_moments(float(node1_k))
        m2, sig2 = compute_node_moments(float(node2_k))
        return y_obs >= abs(m1 + alpha*sig1) or y_obs >= abs(m2 + alpha*sig2)

    flavor_network_w_degree = SGraph()
    new_node_list = flavor_network.vertices.fillna('deg', 0)
    flavor_network_w_degree = flavor_network_w_degree.add_vertices(new_node_list).add_edges(edges)
    flavor_network_w_degree = flavor_network_w_degree.triple_apply(degree_count_fn, mutated_fields=['deg'])
    weights_dict = flavor_network_w_degree.vertices.to_dataframe().set_index('__id').to_dict()['deg']

    significant_edges = []
    for edge in edges:
        if test_for_significance(edge, weights_dict, alpha):
            significant_edges.append(edge)
    pruned_network = SGraph().add_vertices(new_node_list)
    pruned_network = pruned_network.add_edges(significant_edges)
    return significant_edges, pruned_network

if __name__ == '__main__':
    with open('../../notebooks/data/first_ing_comp_dict.pkl', 'r') as f:
        icd = pickle.load(f)
    fnet = extract_backbone(build_weighted_graph(icd))