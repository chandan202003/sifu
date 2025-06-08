# Quick Start

This guide will help you get started with Sifu in just a few minutes.

## Installation

First, install Sifu using pip:

```bash
pip install sifu-ai
```

## Basic Usage

### Initializing Sifu

```python
from sifu import Sifu
import asyncio

async def main():
    # Initialize Sifu
    sifu = Sifu()
    
    # Process a query
    response = await sifu.process_query("Hello, what can you do?")
    print(f"Response: {response['text']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Adding Knowledge

```python
# Add knowledge to the knowledge base
entry = await sifu.knowledge_base.add_entry(
    content="Sifu is an advanced AI assistant",
    metadata={"category": "introduction"},
    tags=["ai", "assistant"],
    language="en"
)
```

### Querying Knowledge

```python
# Search the knowledge base
results = await sifu.knowledge_base.search("What is Sifu?")
for result in results:
    print(f"- {result.content} (Score: {result.score:.2f})")
```

### Using Context

```python
# Create a conversation with context
context = {"user_id": "123", "conversation_id": "456"}

# First message
response1 = await sifu.process_query("My name is Alice", context)
print(f"Sifu: {response1['text']}")

# Second message (context is maintained)
response2 = await sifu.process_query("What's my name?", context)
print(f"Sifu: {response2['text']}")  # Will remember the name from context
```

## Command Line Interface

Sifu comes with a simple CLI:

```bash
# Start an interactive session
sifu chat

# Process a single query
sifu query "What can you do?"

# Add knowledge from a file
sifu add-knowledge --file knowledge.json
```

## Web API

Start the web server:

```bash
uvicorn sifu.api:app --reload
```

Then access the API at `http://localhost:8000`

### Example API Requests

```bash
# Health check
curl http://localhost:8000/health

# Process a query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, what can you do?"}'

# Add knowledge
curl -X POST http://localhost:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{"content": "Sifu is an AI assistant", "tags": ["ai"]}'
```

## Configuration

Create a `.env` file in your project root:

```env
# Database settings
DATABASE_URL=sqlite:///sifu.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/sifu.log

# API settings
API_KEY=your_api_key
HOST=0.0.0.0
PORT=8000

# Model settings
MODEL_NAME=all-MiniLM-L6-v2
SIMILARITY_THRESHOLD=0.7
```

## Next Steps

- Explore the [User Guide](../user_guide/core_concepts.md) for detailed documentation
- Check out [Examples](../examples/basic_usage.md) for more code samples
- Read the [API Reference](../api_reference/overview.md) for complete API documentation

## Getting Help

- [GitHub Issues](https://github.com/yourusername/sifu/issues)
- [Discord Community](https://discord.gg/your-invite-link)
- Email: support@sifu-ai.example.com
