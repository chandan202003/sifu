.PHONY: install dev prod test lint format clean help

# Variables
PYTHON = python3
PIP = pip3
VENV = venv
PYTEST = $(VENV)/bin/pytest
BLACK = $(VENV)/bin/black
ISORT = $(VENV)/bin/isort
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy

# Default target
help:
	@echo "Sifu - Make Commands"
	@echo ""
	@echo "  make install    Install development dependencies"
	@echo "  make dev        Set up development environment"
	@echo "  make prod       Install production dependencies"
	@echo "  make test       Run tests"
	@echo "  make test-cov   Run tests with coverage"
	@echo "  make lint       Run all linters"
	@echo "  make format     Format code with black and isort"
	@echo "  make clean      Clean up temporary files"
	@echo "  make run        Run the API server"
	@echo "  make docs       Build documentation"

# Install development dependencies
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements/dev.txt
	$(PYTHON) -m spacy download en_core_web_sm
	$(PYTHON) -m spacy download xx_ent_wiki_sm
	$(PYTHON) -c "import nltk; nltk.download('punkt')"

# Set up development environment
dev: install
	$(PYTHON) -m pre_commit install

# Install production dependencies
prod:
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements/prod.txt

# Run tests
test:
	$(PYTEST) tests/ -v

# Run tests with coverage
test-cov:
	$(PYTEST) tests/ -v --cov=sifu --cov-report=term-missing --cov-report=xml

# Run linters
lint: black isort flake8 mypy

# Format code
format:
	$(BLACK) sifu/ tests/ examples/
	$(ISORT) sifu/ tests/ examples/

# Check black formatting
black:
	$(BLACK) --check sifu/ tests/ examples/

# Check import sorting
isort:
	$(ISORT) --check-only sifu/ tests/ examples/

# Run flake8
flake8:
	$(FLAKE8) sifu/ tests/ examples/

# Run mypy
mypy:
	$(MYPY) sifu/ tests/ examples/

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	rm -f .coverage

docs:
	@echo "Building documentation..."
	@$(VENV)/bin/mkdocs build

# Run the API server
run:
	uvicorn sifu.api:app --reload
