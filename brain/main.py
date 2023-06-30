from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import routes.getDocData as getDocData_route
import json
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PORT = os.getenv("PORT") or 5000

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/getDocData', methods=['POST'])
@cross_origin()
def getDocData():
    data = request.get_json()
    id = data['id']
    
    return jsonify(getDocData_route.getDocData(id))

@app.route('/')
@cross_origin()
def index():
    return "The brain is running! (this is for graphy the knowledge graph) :D"

if __name__ == '__main__':
    print("Starting server...")
    app.run(debug=True, host='localhost', port=PORT)