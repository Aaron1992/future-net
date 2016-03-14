import numpy as np
from copy import deepcopy

M = np.int_(1000)
topo_file = "topo.csv"
demand_file = "demand.csv"

def read_topo():
    link_array = np.loadtxt(topo_file, dtype=int, delimiter=",")
    with open(demand_file) as f:
        text = f.read()
        start, end, nodes = text.split(",")
        start = np.int_(start)
        end = np.int_(end)
        demand_nodes = np.array(nodes.split("|"),dtype=int)
        demand = {"start": start,
                "end": end,
                "nodes": demand_nodes}

    max_node = max(np.amax(link_array, 0)[1:3])
    node_num = max_node + 1
    m_dis = np.full((max_node+1, max_node +1), M)
    for link in link_array:
        m_dis[link[1], link[2]] = link[3]
    return link_array, demand


