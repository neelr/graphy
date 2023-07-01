# brain

The brain handles the graph fetching, clustering, and AI for the knowledge graph! 

**Routes:**  
- `/getDocData` - returns the document data from the brain via the id
- `/putDoc` - puts the document into the brain
- `/recomputeGraph` - recomputes the graph and saves it

**Environment Variables:**  
- `OPENAI_API_KEY` - the openai api key
- `PINECONE_API_KEY` - the pinecone api key
- `PINECONE_ENV` - the pinecone environment
- `PINECONE_INDEX` - the pinecone index
- `PORT` - the port to run the server on (default: 5000)

