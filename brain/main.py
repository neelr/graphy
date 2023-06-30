from dotenv import load_dotenv
from flask import Flask, request, jsonify
import logging, sys
from flask_cors import CORS, cross_origin
import routes.getDocData as getDocData_route
import routes.putDoc as putDoc_route
import json
import os
load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PORT = os.getenv("PORT") or 5000

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

"""
    /getDocData
    {
        "id": string
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

    return jsonify(getDocData_route.getDocData(id))


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

@app.route('/')
@cross_origin()
def index():
    return "The brain is running! (this is for graphy the knowledge graph) :D"

if __name__ == '__main__':
    print("Starting server...")
    app.run(debug=True, host='localhost', port=PORT)