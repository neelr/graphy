import networkx as nx
import hashlib
import time
import matplotlib.pyplot as plt
import matplotlib

def init():
    global graph
    graph = nx.Graph()

def clear():
    global graph
    graph.clear()

def add_node(id, title, metadata, embedding):
    global graph
    graph.add_node(id, title=title, metadata=metadata, embedding=embedding)

def add_edge(id1, id2, weight=1):
    global graph
    graph.add_edge(id1, id2, weight=weight)

def save_visualization(labels):
    global graph
    matplotlib.use('Qt5Agg')
    plt.figure(figsize=(20,20))
    # no labels
    nx.draw_networkx(graph, with_labels=False, node_size=10, width=0.1, alpha=0.5, node_color=labels, cmap="tab20")

    # save to static folder
    plt.savefig(f"./static/graph_{hashlib.sha256(str(time.time()).encode()).hexdigest()}.png")