# Ollama + Weaviate Local Setup

## Installation
Only 6 steps are needed to set up a local environment with Ollama and Weaviate. The following instructions are for a Unix-based system.
### Requirements
1. [Ollama](https://ollama.com/).
2. [Docker](https://docs.docker.com/get-docker/).
3. Python 3.10 or higher.

Then, you can use the Makefile to install the required dependencies. The makefile has the following commands:
- `make install`: Install the required dependencies.
- `make docker_start`: Set up and start the Weaviate Docker instance.
- `make easyfnc_setup`: Clone the EasyFNC repository and install requirements.
- `make run`: Run the script.
- `make run_api`: Run the FastAPI app.
- `make docker_stop`: Stop the Weaviate Docker instance.
- `make clean`: Remove the virtual environment and its contents.

A typical installation would look like this:
```bash
make install
make easyfnc_setup
make docker_start
```

## Usage

Simply run the script with the following command:
```bash
make run
```
To run the FastAPI app, use the following command:
```bash
make run_api
```
After you are done, you can stop the Weaviate Docker instance with:
```bash
make docker_stop
```
Additionally, you can clean up the virtual environment with:
```bash
make clean
```