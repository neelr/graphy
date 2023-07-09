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


def getNodeLinkData(g):
    data = nx.node_link_data(g)

    # remove embedding from nodes
    for i in data["nodes"]:
        i.pop("embedding", None)

    return data["nodes"], data["links"]


def getSubGraphData(g, nodes):
    g = g.subgraph(nodes)
    return getNodeLinkData(g)


"""
    getAdjacencyDataNodes(clusters, query)
    clusters: list of cluster ids
    query: string

    returns: {
        "nodes": list,
        "links": list,
    }

    returns the nodes and links in the cluster for a graph
"""


def getAdjacencyDataNodes(clusters, query):
    global graph
    global clusterGraph
    nodes = []

    # if clusters == None then get all nodes
    if clusters == None or len(clusters) == 0:
        clusters = [i[0] for i in clusterGraph.nodes.data("id")]

    # get all nodes in the clusters
    for i in clusters:
        nodes += clusterGraph.nodes[i]["metadata"]["documents"]

    # get subgraph with only the nodes in the clusters
    nodes, links = getSubGraphData(graph, nodes)

    # check content for query
    if query != "" and query != None:
        nodes = [i for i in nodes if query.lower() in i["metadata"]
                 ["text"].lower()]

    nodes, links = getSubGraphData(graph, [i["id"] for i in nodes])

    return nodes, links


"""
    getAdjacencyDataClusters(query)
    clusters: list of cluster ids
    query: string

    returns: {
        "nodes": list,
        "links": list,
    }
"""


def getAdjacencyDataClusters(clusters, query):
    global clusterGraph
    nodes = []
    links = []
    print(clusters)

    if clusters != None and len(clusters) != 0:
        nodes, links = getSubGraphData(clusterGraph, clusters)
    else:
        nodes, links = getNodeLinkData(clusterGraph)

    # check content for query
    if query != "" and query != None:
        nodes = [i for i in nodes if query.lower() in i["metadata"]
                 ["summary"].lower()]

    nodes, links = getSubGraphData(clusterGraph, [i["id"] for i in nodes]) 

    return nodes, links


def normalize(x, newRange=(0, 1)):  # x is an array. Default range is between zero and one
    x = np.array(x)  # convert input into an array
    print(x)
    xmin, xmax = np.min(x), np.max(x)  # get max and min from input array
    norm = (x - xmin)/(xmax - xmin)  # scale between zero and one

    if newRange == (0, 1):
        return (norm)  # wanted range is the same as norm
    elif newRange != (0, 1):
        # scale to a different range.
        return norm * (newRange[1] - newRange[0]) + newRange[0]


def save_visualization(labels):
    global graph
    global clusterGraph
    matplotlib.use('Qt5Agg')

    def plot(g):
        plt.figure(figsize=(20, 20))
        if g.graph['name'] == "clusterGraph":
            print(list(g.nodes.data('metadata')))
        # no labels
        titles = nx.get_node_attributes(g, 'title')
        nx.draw_networkx(g, labels=titles, node_size=300 if g.graph['name'] == "graph" else normalize([len(i[1]["documents"]) for i in g.nodes.data(
            'metadata')], newRange=(0, 1000)),  width=0.1, alpha=0.5, node_color=labels if g.graph['name'] == "graph" else [1]*len(g.nodes), cmap='viridis')

        # save to static folder
        plt.savefig(
            f"./static/{g.graph['name']}_{time.strftime('%Y_%m_%d-%H-%M-%S')}.png")

        # clear plot
        plt.clf()
    plot(graph)
    plot(clusterGraph)
