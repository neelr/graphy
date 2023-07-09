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
    query(qs)
    qs: // Pinecone Query

    returns: {
        "error": string,
        "nodes": list,
        "links": list,
    }
"""
def query(qs):
    search = index.query(
        vector=[0]*768,
        top_k=1e4,
        filter=qs,
    )["matches"]

    nodes, links = graphData.getSubGraphData(graphData.graph, [i["id"] for i in search])

    return {
        "error": "",
        "nodes": nodes,
        "links": links
    }

    