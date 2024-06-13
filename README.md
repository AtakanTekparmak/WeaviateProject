# Ollama + Weaviate Local Setup

## What to expect

This project is an Ollama + Streamlit + FastAPI app that allows the user to ask an LLM to perform basic CRUD operations on a FastAPI server given the user's input, the database schemas and the available tools (create, read, update, delete). 

## Demo Video

![Demo Video](streamlit_demo.mov)

## Installation
Only a few steps are needed to set up a local environment with Ollama and Weaviate. The following instructions are for a Unix-based system.
### Requirements
1. [Ollama](https://ollama.com/).
2. [Docker](https://docs.docker.com/get-docker/).
3. Python 3.10 or higher.

Then, you can use the Makefile to install the required dependencies. The makefile has the following commands:
- `make install`: Install the required dependencies.
- `make docker_start`: Set up and start the Weaviate Docker instance.
- `make run_api`: Run the FastAPI app.
- `make run`: Run the Streamlit app.
- `make docker_stop`: Stop the Weaviate Docker instance.
- `make clean`: Remove the virtual environment and its contents.

A typical installation would look like this:
```bash
make install
make docker_start
```

## Usage

To run the FastAPI app, use the following command:
```bash
make run_api
```
Then, you can run the Streamlit app with:
```bash
make run
```
After you are done, you can stop the Weaviate Docker instance with:
```bash
make docker_stop
```
Additionally, you can clean up the virtual environment with:
```bash
make clean
```
