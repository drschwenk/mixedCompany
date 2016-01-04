import graphlab as gl
from graphlab import SGraph, Vertex, Edge, degree_counting, connected_components
import cPickle as pickle


def build_weighted_graph(ing_comp_dict):
    """
    builds the weighted undirected graph that is the flavor network
    :param ing_comp_dict: ingredient:compound dictionary
    :return: SGraph that represents the flavor network
    """

    def degree_count_fn (src, edge, dst):
        """
        increments the degree of the nodes on this edge
        :param src:
        :param edge:
        :param dst:
        :return:
        """
        src['deg'] += 1
        dst['deg'] += 1
        return (src, edge, dst)

    flav_network = SGraph()
    vert_list = []
    edge_list = []
    ingrds_not_seen = ing_comp_dict.keys()
    for node_1_ingr, compounds in ing_comp_dict.iteritems():
        ingrds_not_seen.remove(node_1_ingr)
        vert_list.append(Vertex(node_1_ingr, attr={'deg': 0}))
        for node_2_ingr in ingrds_not_seen:
            weight = len(set(ing_comp_dict[node_2_ingr]).intersection(set(compounds)))
            if weight > 0:
                edge_list.append(Edge(node_1_ingr, node_2_ingr, attr={'weight': weight}))
        vert_list.append(Vertex(node_1_ingr))

    flav_network = flav_network.add_vertices(vert_list)
    flav_network = flav_network.add_edges(edge_list)
    flav_net_w_deg = SGraph()
    new_node_list = flav_network.vertices.fillna('deg', 0)
    flav_net_w_deg = flav_net_w_deg.add_vertices(new_node_list).add_edges(edge_list)
    flav_net = flav_net_w_deg.triple_apply(degree_count_fn, mutated_fields=['deg'])

    return flav_net


# with open('./data/first_ing_comp_dict.pkl', 'r') as f:
#     ing_comp_dict = pickle.load(f)