import pinecone
from dotenv import load_dotenv
import os
import logging
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
    getDocData(id)
    id: string

    returns: {
        "id": string,
        "data": dict,
        "embedding": list,
        "error": string
    }

    returns the document data from the index
"""
def getDocData(id):

    doc = index.fetch(ids=[id], namespace="uno")

    logging.info(f"fetched doc: {doc}")

    vectors = doc["vectors"]

    if len(dict.keys(vectors)) == 0:
        return {
            "id": "",
            "data": {},
            "embedding": [],
            "error": "Document not found"
        }
    
    doc = list(vectors.values())

    return {
        "id": doc[0]["id"],
        "data": doc[0]["metadata"],
        "embedding": doc[0]["values"],
        "error": None
    }
