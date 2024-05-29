# Makefile for Ollama + Weaviate Local Setup

# Set default target
.DEFAULT_GOAL := help

# Variables

## Ollama 
EMBEDDING_MODEL := snowflake-arctic-embed:137m
LLM := mistral:7b-instruct-v0.3-fp16

## Python
PYTHON := python3
PIP := pip3
VENV_NAME := venv

## Docker
CONTAINER_NAME := weaviate-container
CONTAINER_IMAGE := cr.weaviate.io/semitechnologies/weaviate:1.24.8

# EasyFNC
EASYFNC_REPO_URL := https://github.com/AtakanTekparmak/EasyFNC.git
EASYFNC_REPO_DIR := EasyFNC
EASYFNC_SOURCE_DIR := easy_fnc

# Help target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  1. install        Install dependencies and set up the environment (should be run first)"
	@echo "  2. docker_start   Set up and start the Weaviate Docker container (should be run second, before run)"
	@echo "  3. easyfnc_setup  Clone the AtakanTekparmak/EasyFNC repository and install requirements (should be run third, after install and docker_start)"
	@echo "  4. run            Run the main.py script (should be run after install, docker_start, and easyfnc_setup)"
	@echo "  5. run_api        Run the FastAPI app"
	@echo "  6. docker_stop    Stop the Weaviate Docker container (should be run last after run)"
	@echo "  7. clean          Remove the virtual environment and its contents"

# Install dependencies and set up the environment
install:
	$(PYTHON) -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && \
	ollama pull $(EMBEDDING_MODEL) && \
	ollama pull $(LLM) && \
	$(PIP) install -r requirements.txt

# Run the main.py script
run:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) main.py

# Clean the virtual environment
clean:
	rm -rf $(VENV_NAME)

# Set up the Weaviate Docker container
docker_start:
	@docker container inspect $(CONTAINER_NAME) >/dev/null 2>&1 && \
		(echo "Restarting Docker container $(CONTAINER_NAME)" && \
		docker restart $(CONTAINER_NAME)) || \
		(echo "Creating Docker container $(CONTAINER_NAME)" && \
		docker run -d --name $(CONTAINER_NAME) -p 8080:8080 -p 50051:50051 $(CONTAINER_IMAGE))
	@docker container inspect $(CONTAINER_NAME) >/dev/null 2>&1 || \
		(echo "Failed to create Docker container $(CONTAINER_NAME)" && exit 1)
	@echo "Docker container $(CONTAINER_NAME) is running"

# Stop the Weaviate Docker container
docker_stop:
	@docker stop $(CONTAINER_NAME) || \
		(echo "Docker container $(CONTAINER_NAME) is not running" && exit 0)
	@echo "Docker container $(CONTAINER_NAME) has been stopped"

# Clone the git repository and install requirements
easyfnc_setup:
	@git clone $(EASYFNC_REPO_URL) $(EASYFNC_REPO_DIR)
	@cd $(EASYFNC_REPO_DIR) && \
		. ../$(VENV_NAME)/bin/activate && \
		$(PIP) install -r requirements.txt
	@mv $(EASYFNC_REPO_DIR)/$(EASYFNC_SOURCE_DIR) . && rm -rf $(EASYFNC_REPO_DIR)

# Run the FastAPI app
run_api:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) src/main.py