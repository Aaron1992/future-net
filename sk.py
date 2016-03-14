from lib import read_topo, M
from dijkstra import Dijkstra, shortestPath as shortest_path
import crash_on_ipy
from ipdb import set_trace
import timeit

KEEP_MAX = 100
DEBUG = False


graph = {}
topo, demand = read_topo()
t_start = timeit.default_timer()

for arc in topo:
    if not arc[1] in graph:
        graph[arc[1]] = {}
    graph[arc[1]][arc[2]] = arc[3]

if DEBUG:
    print(graph)
    print(demand)
    print(Dijkstra(graph,2))
    print(shortest_path(graph, 5, 17))
s = demand["start"]
t = demand["end"]
Vs = demand["nodes"]
Vs_num = len(Vs)
Dis = {s:{}}
F =[]
f = {}
for vi in demand["nodes"]:
    Dis[s][vi] = shortest_path(graph, s, vi)
    f[vi] = [shortest_path(graph, vi, t)]
    if vi not in Dis:
        Dis[vi] = {}
    for vl in demand["nodes"]:
        if vl != vi:
            Dis[vi][vl] = shortest_path(graph, vi, vl)
F.append(f)

def add_point(p1, p2):
    p = {"cost":0,
            "path":[]}
    p["path"] = p1["path"] + p2["path"][1:]
    p["cost"] = p1["cost"] + p2["cost"]
    checked = []

    #check loop
    for n in p["path"]:
        if n in checked:
            return None
        else:
            checked.append(n)
    return p

def count_sp_nodes(p):
    count = 0
    for n in p["path"][1:]:
        if n in Vs:
            count += 1
    return count


if DEBUG:
    print('-'*20)
    for v,fv in f.items():
        print(v, fv)
    print('-'*20)

for k in range(1, Vs_num):
    print("Gen : ",k)
    f = {}
    for vi in Vs:
        min_f =[]
        for vl,f_vl in F[k-1].items():
            if vi == vl:
                continue
            for f_vl_item in f_vl:
                temp = add_point(Dis[vi][vl], f_vl_item)
                if temp and count_sp_nodes(temp) >= k:
                    min_f.append(temp)
        f[vi] = sorted(min_f,key=lambda k:k["cost"])[:KEEP_MAX]
        if k==1 and vi==13:
            pass
    F.append(f)

    if DEBUG:
        for v,fv in f.items():
            print(v,len(fv), fv[:1])
        print('-'*20)


# last step
# vi = s

min_f = []
for vl, f_vl in F[Vs_num-1].items():
    for f_vl_item in f_vl:
        temp = add_point(Dis[s][vl], f_vl_item)
        if temp and count_sp_nodes(temp) >= k:
            min_f.append(temp)
f[s] = sorted(min_f,key=lambda k:k["cost"])[:5]
print(f[s])

t_end = timeit.default_timer()
print(t_end - t_start)
