from easy_fnc.models.ollama import OllamaModel
from easy_fnc.function_caller import FunctionCaller
from easy_fnc.utils import load_template
import json

# Set constants
MODEL_NAME = "yi:34b-chat-v1.5-q8_0" # using llama3 model for testing
VERBOSE = True
SHOW_FUNCTION_CALLS = True

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

user_query = "Can you add a driver to the database?"
#user_query = "Can you add a 2022 Opel Astra to the database?"
print(f"-User Input: \n{user_query}\n")
function_calls = model.get_function_calls(prefix_string + user_query, verbose=SHOW_FUNCTION_CALLS)

# Call the functions
output = ""
for function in function_calls:
    output = function_caller.call_function(function)
    if VERBOSE:
        print(f"Function Output: {output}")

# Call the model with the output
if isinstance(output, int):
    response = "Sure, created record with ID: " + str(output)
else:
    response = model.generate(output, first_message=False, response_message=True, original_prompt=user_query) if output else "Function output is empty"

# Print the response
print(f"- Model reply: \n{response}")
