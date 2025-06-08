#!/bin/bash
# Sifu Setup Script
# This script sets up the development environment for Sifu

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is required but not installed. Please install Python 3.8+ and try again.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$PYTHON_VERSION" < "3.8" ]]; then
    echo -e "${YELLOW}Sifu requires Python 3.8 or higher. Found Python $PYTHON_VERSION.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION is installed${NC}"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Install development dependencies if --dev flag is passed
    if [[ "$1" == "--dev" ]]; then
        echo -e "${GREEN}Installing development dependencies...${NC}"
        pip install -r requirements/dev.txt
    fi
    
    # Install production dependencies if --prod flag is passed
    if [[ "$1" == "--prod" ]]; then
        echo -e "${GREEN}Installing production dependencies...${NC}"
        pip install -r requirements/prod.txt
    fi
    
    # Install language models
    echo -e "${GREEN}Downloading language models...${NC}"
    python -m spacy download en_core_web_sm
    python -m spacy download xx_ent_wiki_sm
    
    # Install NLTK data
    python -c "import nltk; nltk.download('punkt')"
    
    echo -e "${GREEN}✓ Virtual environment setup complete${NC}"
else
    echo -e "${GREEN}Virtual environment already exists${NC}"
    source venv/bin/activate
fi

# Set up pre-commit hooks
if [[ "$1" == "--dev" ]]; then
    echo -e "${GREEN}Setting up pre-commit hooks...${NC}"
    pre-commit install
fi

echo -e "\n${GREEN}🎉 Setup complete!${NC}"
echo -e "To activate the virtual environment, run: ${YELLOW}source venv/bin/activate${NC}"
echo -e "To run the API server: ${YELLOW}uvicorn sifu.api:app --reload${NC}"
echo -e "To run tests: ${YELLOW}pytest tests/${NC}"

# Run the example if no arguments are provided
if [ $# -eq 0 ]; then
    echo -e "\n${GREEN}Running example script...${NC}"
    python -m examples.basic_usage
fi
