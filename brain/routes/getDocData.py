import pinecone
from dotenv import load_dotenv
import os
import logging
import json
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
    getSimilar: bool # optional (default: true)
    k: int # optional (default: 3)

    returns: {
        "id": string,
        "data": dict,
        "embedding": list,
        "similar_docs": list,
        "error": string
    }

    returns the document data from the index and the similar docs
"""
def getDocData(id, getSimilar=True, k=3):
    if id == "":
        return {
            "id": "",
            "data": {},
            "embedding": [],
            "error": "Document not found"
        }

    doc = index.fetch(ids=[id], namespace="uno")

    logging.info(f"fetched docs for id {id}")

    vectors = doc["vectors"]

    if len(dict.keys(vectors)) == 0:
        return {
            "id": "",
            "data": {},
            "embedding": [],
            "error": "Document not found"
        }
    
    doc = list(vectors.values())

    similar_docs = []

    if getSimilar:
        # get similar docs
        similar_docs = index.query(
            vector=doc[0]["values"],
            top_k=k+1,
            include_metadata=True,
            namespace="uno"
        )["matches"]

        similar_docs = [{
            "id": i["id"],
            "title": i["metadata"]["title"],
            #"tags": i["metadata"]["tags"],
            #"ptr": i["metadata"]["ptr"],
            "similarity": i["score"],
        } for i in similar_docs if i["id"] != doc[0]["id"]]

    return {
        "id": doc[0]["id"],
        "data": doc[0]["metadata"],
        "embedding": doc[0]["values"],
        "similar_docs": similar_docs,
        "error": None
    }
