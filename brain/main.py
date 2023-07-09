from dotenv import load_dotenv
from flask import Flask, request, jsonify
import logging, sys
from flask_cors import CORS, cross_origin
import helpers.graphData as graphData
import routes.getDocData as getDocData_route
import routes.putDoc as putDoc_route
import routes.recomputeGraph as recomputeGraph_route
import routes.getAdjacencyData as getAdjacencyData_route
import routes.query as query_route
import json
import os
load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PORT = os.getenv("PORT") or 5000

graphData.init()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

"""
    /getDocData
    {
        "id": string,
        "getSimilar": bool # optional (default: true),
        "k": int # optional (default: 3)
    }

    returns: {
        "id": string,
        "data": dict,
        "embedding": list,
        "error": string
    }

    returns the document data from the brain via the id
"""
@app.route('/getDocData', methods=['POST'])
@cross_origin()
def getDocData():
    data = request.get_json()
    id = data['id']
    getSimilar = data['getSimilar'] if 'getSimilar' in data else True
    k = data['k'] if 'k' in data else 3

    return jsonify(getDocData_route.getDocData(id, getSimilar, k))


"""
    /putDoc
    {
        "title": string,
        "ptr": string, # usually a url 
        "tags": list, # additonal tags
        "content": string
    }

    returns: {
        "id": string,
        "title": string,
        "ptr": string,
        "tags": list,
        "content": string,
        "error": string
    }

    puts the document into the brain
"""
@app.route('/putDoc', methods=['POST'])
@cross_origin()
def putDoc():
    data = request.get_json()
    title = data['title']
    ptr = data['ptr']
    tags = data['tags']
    content = data['content']

    return jsonify(putDoc_route.putDoc(title, ptr, tags, content))

"""
    /recomputeGraph

    returns: {
        "error": string,
        "message": string,
        "centroids": list
    }

    recomputes the graph and saves it
"""
@app.route('/recomputeGraph', methods=['GET'])
@cross_origin()
def recomputeGraph():
    return jsonify(recomputeGraph_route.recomputeGraph())

"""
    /getAdjacencyData
    {
        "resolution": "node" | "cluster",
        "clusters": list # optional (default: all clusters),
        "query": string # optional (default: all nodes)
    }

    returns: {
        "error": string,
        "nodes": list,
        "links": list,
    }
"""
@app.route('/getAdjacencyData', methods=['POST'])
@cross_origin()
def getAdjacencyData():
    data = request.get_json()
    resolution = data['resolution']
    clusters = data['clusters'] if 'clusters' in data else None
    query = data['query'] if 'query' in data else None
    nodes = data['nodes'] if 'nodes' in data else None

    return jsonify(getAdjacencyData_route.getAdjacencyData(resolution, clusters, nodes, query))

"""
    /query
    {
        "filter": {
            // PINECONE FILTERS
        }
    }

    returns: {
        "error": string,
        "nodes": list,
        "links": list,
    }
"""
@app.route('/query', methods=['POST'])
@cross_origin()
def query():
    data = request.get_json()
    qs = data['qs']

    return jsonify(query_route.query(qs))

@app.route('/')
@cross_origin()
def index():
    return "The brain is running! (this is for graphy the knowledge graph) :D"

if __name__ == '__main__':
    print("Starting server...")
    app.run(debug=True, host='localhost', port=PORT)