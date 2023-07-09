import pinecone
from dotenv import load_dotenv
import os
import logging
import json
import sys
# setting path
sys.path.append('../helpers')
import helpers.graphData as graphData
load_dotenv("../.env")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)


index = pinecone.Index(PINECONE_INDEX)

"""
    getAdjacencyData(resolution, clusters, query)
    resolution: "nodes" or "clusters"
    clusters: list of cluster ids
    nodes: list of node ids
    query: string

    returns: {
        "error": string,
        "nodes": list,
        "links": list,
    }
"""
def getAdjacencyData(resolution, clusters=[], nodes=[], query=""):
    if nodes != None:
        nodes, links = graphData.getSubGraphData(graphData.graph, nodes)
    elif resolution == "nodes":
        nodes, links = graphData.getAdjacencyDataNodes(clusters, query)
    elif resolution == "clusters":
        nodes, links = graphData.getAdjacencyDataClusters(clusters, query)
    else:
        return {
            "error": "Invalid resolution"
        }
    
    return {
        "error": "",
        "nodes": nodes,
        "links": links
    }