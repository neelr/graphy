import networkx as nx
import hashlib
import time
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pickle

def init():
    global graph
    global clusterGraph
    graph = nx.Graph(name="graph")
    clusterGraph = nx.Graph(name="clusterGraph")

    if not os.path.exists("./cache"):
        os.makedirs("./cache")

    if os.path.exists("./cache/graphData.graph"):
        load()

def save():
    global graph
    global clusterGraph
    pickle.dump(graph, open("./cache/graphData.graph", "wb"))
    pickle.dump(clusterGraph, open("./cache/clusterGraphData.graph", "wb"))

def load():
    global graph
    global clusterGraph
    graph = pickle.load(open("./cache/graphData.graph", "rb"))
    clusterGraph = pickle.load(open("./cache/clusterGraphData.graph", "rb"))

def clear():
    global graph
    global clusterGraph
    graph.clear()
    clusterGraph.clear()

    graph.graph["name"] = "graph"
    clusterGraph.graph["name"] = "clusterGraph"

def normalize(x, newRange=(0, 1)): #x is an array. Default range is between zero and one
    x = np.array(x) #convert input into an array
    print(x)
    xmin, xmax = np.min(x), np.max(x) #get max and min from input array
    norm = (x - xmin)/(xmax - xmin) # scale between zero and one
    
    if newRange == (0, 1):
        return(norm) # wanted range is the same as norm
    elif newRange != (0, 1):
        return norm * (newRange[1] - newRange[0]) + newRange[0] #scale to a different range.    


def save_visualization(labels):
    global graph
    global clusterGraph
    matplotlib.use('Qt5Agg')
    def plot(g):
        plt.figure(figsize=(20,20))
        if g.graph['name'] == "clusterGraph":
            print(list(g.nodes.data('metadata')))
        # no labels
        titles = nx.get_node_attributes(g, 'title') 
        nx.draw_networkx(g, labels=titles, node_size=300 if g.graph['name'] == "graph" else normalize([len(i[1]["documents"]) for i in g.nodes.data('metadata')], newRange=(0, 1000)),  width=0.1, alpha=0.5, node_color=labels if g.graph['name'] == "graph" else [1]*len(g.nodes), cmap='viridis')

        # save to static folder
        plt.savefig(f"./static/{g.graph['name']}_{time.strftime('%Y_%m_%d-%H-%M-%S')}.png")

        # clear plot
        plt.clf()
    plot(graph)
    plot(clusterGraph)