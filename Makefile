# Makefile for Ollama + Weaviate Local Setup

# Set default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
VENV_NAME := venv

# Help target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  1. install       Install dependencies and set up the environment (should be run first)"
	@echo "  2. docker_setup  Set up the Weaviate Docker container (should be run second, before run)"
	@echo "  3. run           Run the main.py script (should be run third, after install and docker_setup)"
	@echo "  4. docker_stop   Stop the Weaviate Docker container (should be run last after run)"
	@echo "  5. clean         Remove the virtual environment and its contents"

# Install dependencies and set up the environment
install:
	$(PYTHON) -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && \
	ollama pull snowflake-arctic-embed:137m && \
	ollama pull llama3:8b-instruct-fp16 && \
	$(PIP) install -r requirements.txt

# Run the main.py script
run:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) main.py

# Clean the virtual environment
clean:
	rm -rf $(VENV_NAME)

# Set up the Weaviate Docker container
docker_setup:
	docker run -d -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:1.24.8

# Stop the Weaviate Docker container
docker_stop:
	docker stop $$(docker ps -q --filter="ancestor=cr.weaviate.io/semitechnologies/weaviate:1.24.8")