from src.weaviate import Client
from src.utils import load_config

from easy_fnc.models.ollama import OllamaModel
from easy_fnc.function_caller import FunctionCaller
from easy_fnc.utils import load_template

import streamlit as st
import json

def weaviate_main():
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

def setup() -> tuple[OllamaModel, FunctionCaller, str, str]:
    # Set constants
    #MODEL_NAME = "yi:34b-chat-v1.5-q8_0" # using llama3 model for testing
    MODEL_NAME = "adrienbrault/nous-hermes2pro-llama3-8b:f16"

    # Instantiate a FunctionCaller and add user functions
    function_caller = FunctionCaller()
    function_caller.add_user_functions("functions.py")
    functions_metadata = function_caller.create_functions_metadata()

    # Create a model
    model = OllamaModel(
        model_name=MODEL_NAME,
        functions=functions_metadata,
        template=load_template("template.json"),
    )

    # Load the database schema
    try:
        with open("schema.json") as f:
            database_schema = json.load(f)
    except FileNotFoundError:
        database_schema = {}
        print("Schema file not found")

    # Call the model with a query
    prefix_string = f"The models in the database are like the following (Note, the 'id' field for each model is not needed when creating, but foreign id fields (ex. 'car_id') are needed.) :\n{json.dumps(database_schema, indent=4)}\n\n"
    suffix_string = "\n Note: Think truly about the database schema and the data you are adding. The data should be consistent with the schema and the data already in the database. Look at the relationships and dependencies between the database models."

    return model, function_caller, prefix_string, suffix_string

def streamlit_generate(
        user_query: str,
        model: OllamaModel,
        function_caller: FunctionCaller,
        prefix_string: str,
        suffix_string: str
    ) -> str:
    # Set constants
    VERBOSE = True
    SHOW_FUNCTION_CALLS = True
    #user_query = "Can you add a maintenance report to the database?"

    function_calls = model.get_function_calls(prefix_string + user_query, verbose=SHOW_FUNCTION_CALLS)

    # Call the functions
    output = ""
    for function in function_calls:
        output = function_caller.call_function(function)
        if VERBOSE:
            print(f"Function Output: {output}\n")
    
    st.session_state.messages.append({"role": "assistant", "content": function_calls})
    st.chat_message("assistant").write("Function calls: ")
    st.chat_message("assistant").write(function_calls)

    # Call the model with the output
    if isinstance(output, int):
        response = "Sure, created record with ID: " + str(output)
    else:
        response = model.generate(output, first_message=False, response_message=True, original_prompt=user_query) if output else "Function output is empty"

    # Print the response
    response = f"- Model reply: \n{response}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)


if __name__ == "__main__":
    weaviate_main()