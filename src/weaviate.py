import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import Property, DataType

import ollama

from src.utils import load_config

# Declare constants
DOCUMENTS = [
  "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
  "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
  "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
  "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
  "Llamas are vegetarians and have very efficient digestive systems",
  "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]

class Client:
    """Wrapper class for the Weaviate client."""
    def __init__(self):
        self.client = weaviate.connect_to_local(port=load_config()["weaviate"][0]["PORT"])
    
    def create_collection(self, collection_name: str):
        """Create a new data collection in Weaviate."""
        # Check if the collection already exists
        if self.client.collections.exists(collection_name):
            # Return the existing collection
            return 
        
        # Create a new data collection
        collection = self.client.collections.create(
            name = collection_name,
            properties=[
                Property(name="text", data_type=DataType.TEXT),
            ],
        )
        # Populate the collection with documents
        self.add_documents_to_collection(collection_name, DOCUMENTS)

    def add_documents_to_collection(self, collection_name: str, documents: list[str]):
        """Add documents to a collection in Weaviate."""
        # Get the collection
        collection = self.client.collections.get(collection_name)

        # Store each document in a vector embedding database
        with collection.batch.dynamic() as batch:
            for idx, doc in enumerate(documents):
                # Generate embeddings
                response = ollama.embeddings(model = load_config()["ollama"][0]["OLLAMA_EMBED_MODEL"] , prompt = doc)

                # Add data object with text and embedding
                batch.add_object(
                    properties = {"text" : doc},
                    vector = response["embedding"],
                )

    def retrieve_documents(self, collection_name: str, prompt: str, limit: int = 3):
        # Get the collection
        collection = self.client.collections.get(collection_name)

        # Generate an embedding for the prompt and retrieve the most relevant doc
        response = ollama.embeddings(
            model = load_config()["ollama"][0]["OLLAMA_EMBED_MODEL"],
            prompt = prompt,
        )

        results = collection.query.near_vector(
            near_vector = response["embedding"],
            limit = limit,
        )

        results_text = []
        for result in results.objects:
            results_text.append(result.properties['text'])

        return results_text

    def close(self):
        self.client.close()