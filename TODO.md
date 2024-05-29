# TO-DO List for Weaviate Project

1. [ ] Refine the fastapi app.
    1. [ ] Refine the models (add some real-life examples and relationships).
    2. [ ] Add some logic outside of basic CRUD operations. 
    3. [ ] Refine the endpoints accordingly.
    4. [ ] Add some tests.

2. [ ] Get the FastAPI docs into Weaviate.
    1. [ ] Retrieve the FastAPI docs.
    2. [ ] Separate the FastAPI docs into chunks.
    3. [ ] Add the chunks to Weaviate.
    4. [ ] Add some logic to retrieve the docs from Weaviate (retrieve endpoints and models separately).
    5. [ ] (Optional) Add the LLM part as a module of the FastAPI app then conceal it from the docs when retrieving them.
    6. [ ] Add some tests.
    7. [ ] Edit the Makefile accordingly.

3. [ ] Integrate EasyFNC and function calling.
    1. [ ] Add a functions.py with wrapper functions for the api endpoints so EasyFNC can convert and call them.
    2. [ ] Integrate the retrieved context from Weaviate into the EasyFNC prompt.
    3. [ ] Add some tests.
    4. [ ] Edit the Makefile accordingly.

4. [ ] Refine the Makefile and polish the project

