from src.weaviate import Client, DOCUMENTS
from src.utils import load_config

def main():
    # Create a new Weaviate client
    client = Client()

    # Get or create a collection
    collection_name = load_config()["weaviate"][0]["COLLECTION_NAME"]
    client.create_collection(collection_name)

    # Retrieve documents
    prompt = "Llamas and camels are buddies!"
    results = client.retrieve_documents(collection_name, prompt, limit=2)
    print(results)

    # Close the Weaviate client
    client.close()


if __name__ == "__main__":
    main()