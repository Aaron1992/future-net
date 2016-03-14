import numpy as np
from copy import deepcopy

MAX_DIS = np.int_(1000)
M = MAX_DIS
topo_file = "topo.csv"
demand_file = "demand.csv"

link_array = np.loadtxt(topo_file, dtype=int, delimiter=",")
with open(demand_file) as f:
    text = f.read()
    start, end, nodes = text.split(",")
    start = np.int_(start)
    end = np.int_(end)
    demand_nodes = np.array(nodes.split("|"),dtype=int)
    demand_nodes = [int(n) for n in nodes.split("|")]
    print(start, end, nodes)

max_node = max(np.amax(link_array, 0)[1:3])

node_num = max_node + 1
m_dis = np.full((max_node+1, max_node +1), MAX_DIS)
for link in link_array:
    m_dis[link[1], link[2]] = link[3]
#m_dis[end, start] = 0

print(m_dis)

count = 0
def search(s, visited):
    global count
    visited = deepcopy(visited)
    visited += [s]
    if s == end:
        count += 1
        print(visited)
        return
    if len(visited) != 1 and s in demand_nodes:
        count += 1
        print(visited)
        return
    next_nodes = []
    for t in range(node_num):
        if -1 != m_dis[s][t] and t not in visited:
            next_nodes += [t]
    if len(next_nodes) == 0:
        return
    else:
        for node in next_nodes:
            search(node, visited)

visited = []
#search(2, visited)
for node in demand_nodes:
    pass
    #search(node, visited)

tabu = []
current = start
allowd = deepcopy(demand_nodes) + [start]


def search_next(current):
    min_d = allowd[0]
    min_cost = M
    for  n in range(node_num):
        if n in allowd and m_dis[current][n] < min_cost:
            min_d = n
            min_cost = m_dis[current][n]
    return min_d


for  i in range(len(demand_nodes) + 1):
    print(allowd)
    print(current)
    allowd.remove(current)
    if len(allowd) != 0:
        current = search_next(current)
