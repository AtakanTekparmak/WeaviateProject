from easy_fnc.models.ollama import OllamaModel
from easy_fnc.function_caller import FunctionCaller
from easy_fnc.utils import load_template

# Set constants
MODEL_NAME = "adrienbrault/nous-hermes2pro-llama3-8b:f16" # using llama3 model for testing
VERBOSE = False
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

# Call the model with a query
user_query = "Can you add a 2021 Toyota Corolla to the 'cars' table in the database? (Please only add the car and do nothing else)"
print(f"-User Input: \n{user_query}\n")
function_calls = model.get_function_calls(user_query, verbose=SHOW_FUNCTION_CALLS)

# Call the functions
output = ""
for function in function_calls:
    output = function_caller.call_function(function)
    if VERBOSE:
        print(f"Function Output: {function_caller.call_function(function)}")

# Call the model with the output
response = model.generate(output, first_message=False, response_message=True, original_prompt=user_query) if output else "Function output is empty"

# Print the response
print(f"- Model reply: \n{response}")
