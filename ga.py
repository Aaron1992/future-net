import numpy as np
from lib import read_topo, M
from random import choice
from copy import deepcopy

m_dis, demand = read_topo()

node_num = m_dis.shape[0]
start = demand["start"]
end = demand["end"]

required = np.append(demand["nodes"], [start, end])
#m_dis[end, start] = 0
for i in range(node_num):
    m_dis[end, i] = M


class Gene():

    def __init__(self, source , to, visit):
        self.cat = str(source) + "|" + str(to)
        self.id_ = ".".join([str(v) for v in visit])
        self.s = source
        self.t = to
        self.visit = visit
        self._cal_cost()

    def _cal_cost(self):
        self.cost = 0
        f_ = self.s
        for t_ in self.visit:
            self.cost += m_dis[f_][t_]
            f_ = t_

    def __repr__(self):
        return "<Gene " + self.cat + "("+ str(self.cost) +")<" + self.id_ + ">>"


gene_lib = {}


def add_gene_lib(gene):
    if gene.cat not in gene_lib:
        gene_lib[gene.cat] = []
    for g in gene_lib[gene.cat]:
        if gene.id_ == g.id_:
            return
    gene_lib[gene.cat].append(gene)

class Path():
    reached = []
    visited = []
    gene_list = []
    cost = 0

    def __init__(self):
        self.cost=0
        self.gene_list = []

    @property
    def length(self):
        return len(self.gene_list)

    def add(self, gene):
        self.gene_list.append(gene)

    def _cal_cost(self):
        for i in range(len(self.visited)-1):
            f_ = self.visited[i]
            t_ = self.visited[i+1]
            self.cost += m_dis[f_][t_]

    def __repr__(self):
        return str(self.gene_list)
        #return str(self.visited)  +" length:" + str(self.length) + " cost:" + str(self.cost)

    def is_loopless(self):
        checked = []
        for gene in self.gene_list:
            for v in gene.visit:
                if v not in checked:
                    checked.append(v)
                else:
                    return False
        return True



path_lib = []

for gen in range(2000):
    for i in required:
        path = Path()
        r1 = i
        v =[]
        visited = []
        reached = []
        reached.append(i)
        visited.append(i)
        allowed = [node for node in range(node_num) \
                if m_dis[i][node] < M and node not in visited]
        while  len(reached) != required.size:
            if len(allowed) == 0:
                break
            current = choice(allowed)
            visited.append(current)
            v.append(current)
            if current in required:
                reached.append(current)
                gene = Gene(r1, current, v)
                add_gene_lib(gene)
                path.add(gene)
                #input("continue?")
                r1 = current
                v = []
            allowed = [node for node in range(node_num) \
                if m_dis[current][node] < M and node not in visited]
        path_lib.append(path)

for path in path_lib:
    print(path)
    print(path.is_loopless())

def crossover(p1, p2):
    p1 = deepcopy(p1)
    if len(p2.gene_list) == 0:
        return None
    g2 = choice(p2.gene_list)
    for index, g1 in enumerate(p1.gene_list):
        if g1.cat == g2.cat:
            if g2.cost < g1.cost:
                p1.gene_list[index] = g2
                if p1.is_loopless():
                    return p1
        else:
            temp = deepcopy(p1)
            temp.gene_list.append(g2)
            if temp.is_loopless():
                return p1
    return None



def better(p1, p2):
    if p1.cost > M:
        return False
    if p1.length >= p2.length:
        return True
    if p1.length >= p2.length and p1.cost <= p2.cost:
        return True
    return False


"""
print("------------corssover---------------")
for ind1 in range(len(path_lib)-1):
    if path_lib[ind1].length >=6:
        for ind2 in range(ind1+1,len(path_lib)):
            try:
                child = crossover(path_lib[ind1], path_lib[ind2])
                if child:
                    print(path_lib[ind1])
                    print(child)
            except Exception:
                raise

"""
count = 0
for category in gene_lib:
    count += len(gene_lib[category])
    print(category, gene_lib[category])
print(count)
