# Installation

This guide will help you install Sifu and its dependencies.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- (Optional) Virtual environment (recommended)
- (Optional) Git (for development installations)

## Installation Methods

### 1. Using pip (Recommended)

The easiest way to install Sifu is using pip:

```bash
pip install sifu-ai
```

### 2. From Source

If you want to install the latest development version:

```bash
# Clone the repository
git clone https://github.com/yourusername/sifu.git
cd sifu

# Install in development mode
pip install -e .
```

### 3. Using Docker

For containerized deployment:

```bash
# Build the Docker image
docker build -t sifu .

# Run the container
docker run -p 8000:8000 sifu
```

## Setting Up a Virtual Environment (Recommended)

It's recommended to use a virtual environment to avoid conflicts with other Python packages:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install Sifu
pip install sifu-ai
```

## Installing Dependencies

### Core Dependencies

Core dependencies are installed automatically with Sifu:

```bash
pip install -r requirements.txt
```

### Development Dependencies

For development, install additional dependencies:

```bash
pip install -r requirements/dev.txt
```

### Production Dependencies

For production deployment:

```bash
pip install -r requirements/prod.txt
```

## Language Models

Sifu uses spaCy for NLP tasks. Install the required language models:

```bash
python -m spacy download en_core_web_sm
python -m spacy download xx_ent_wiki_sm  # For multi-language NER

# Install NLTK data
python -c "import nltk; nltk.download('punkt')"
```

## Verifying the Installation

To verify that Sifu is installed correctly:

```python
import sifu
print(f"Sifu version: {sifu.__version__}")
```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade sifu-ai
```

## Troubleshooting

### Common Issues

1. **Permission Errors**
   - Use `pip install --user` or run with administrator privileges
   - Consider using a virtual environment

2. **Missing Dependencies**
   - Ensure all system dependencies are installed
   - On Ubuntu/Debian: `sudo apt-get install python3-dev build-essential`

3. **spaCy Model Errors**
   - Make sure to download the required language models
   - Try reinstalling spaCy: `pip install --force-reinstall spacy`

4. **CUDA Errors**
   - If using GPU, ensure CUDA is properly installed
   - Try setting `CUDA_VISIBLE_DEVICES=""` to force CPU mode

## Next Steps

- [Quick Start Guide](quickstart.md) - Get started with Sifu
- [Configuration](configuration.md) - Learn how to configure Sifu
- [User Guide](../user_guide/core_concepts.md) - Explore Sifu's features in depth
