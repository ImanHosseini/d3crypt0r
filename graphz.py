ghead = """<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.1draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2">
    <graph>"""

gtail = """    </graph>
</gexf>"""

COLS = ["<viz:color r=\"255\"/>","<viz:color b=\"255\"/>","<viz:color r=\"160\" g=\"160\" b=\"160\"/>"]

def node_def(id,col=0):
    return f"<node id=\"{id}\">\n{COLS[col]}\n</node>"

def edge_def(src,dst):
    return f"<edge source=\"{src}\" target=\"{dst}\">\n<viz:color r=\"0\" g=\"0\" b=\"0\" />\n</edge>"

def s2id(state):
    id = 1
    if len(state) == 1:
        id += state[0]
        return id
    if len(state) == 2:
        id += 30
        id += state[0]*30
        id += state[1]
        return id

def recolor(id,nodes,col=1):
    nsp = nodes.split("\n")
    ln = 2 + id*3
    nsp[ln] = COLS[col]
    return "\n".join(nsp)

nds = []
nodes = ""
edges = ""
nc = 0
for i in range(3):
    lvl = []
    for j in range(30**i):
        nd = nc
        nc += 1
        lvl.append(nd)
        nodes = nodes + f"\n{node_def(nd)}"
    nds.append(lvl)
    if i>0:
        for idx,nd in enumerate(lvl):
            edges += f"\n{edge_def(nd,nds[i-1][idx//30])}"

nodes = recolor(0,nodes)

state = list()
for t in range(600):
    if len(state)<2:
        state.append(0)
        nodes = recolor(s2id(state),nodes)
        continue
    if state[len(state)-1] > 28:
        state[len(state)-1]+=1
        nodes = recolor(s2id(state),nodes)
        continue
    state[len(state)-1] += 1
    nodes = recolor(s2id(state),nodes)


open("gr2.gexf","w").write(f"{ghead}<nodes>{nodes}</nodes>\n<edges>{edges}\n</edges>\n{gtail}\n")