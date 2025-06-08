# Welcome to Sifu

<div class="grid cards" markdown>

-   :fontawesome-brands-python: __Python API__

    ---

    Integrate Sifu into your Python applications with our easy-to-use API.

    [Get Started :fontawesome-solid-arrow-right:](getting_started/quickstart.md)

-   :material-api: __REST API__

    ---

    Access Sifu's features through a fully-featured REST API.

    [API Reference :fontawesome-solid-arrow-right:](api_reference/overview.md)

-   :material-book-open-page-variant: __Guides__

    ---

    Learn how to use Sifu's features with our comprehensive guides.

    [View Guides :fontawesome-solid-arrow-right:](user_guide/core_concepts.md)

-   :material-code-tags: __Examples__

    ---

    Explore practical examples to get started quickly.

    [View Examples :fontawesome-solid-arrow-right:](examples/basic_usage.md)

</div>

## What is Sifu?

Sifu is an advanced knowledge and natural language processing system designed to enhance AI assistants with sophisticated context handling, real-time learning, and multi-language support.

## Key Features

- **Natural Language Understanding**: Advanced intent recognition and entity extraction
- **Knowledge Management**: Store and retrieve information with confidence scoring
- **Context Awareness**: Maintain conversation context and history
- **Multi-language Support**: Automatic language detection and translation
- **Learning Engine**: Improve responses through feedback
- **Modular Architecture**: Extensible design for custom components
- **RESTful API**: Easy integration with existing systems

## Quick Start

1. Install Sifu:
   ```bash
   pip install sifu-ai
   ```

2. Basic usage:
   ```python
   from sifu import Sifu
   import asyncio

   async def main():
       sifu = Sifu()
       response = await sifu.process_query("Hello, what can you do?")
       print(response['text'])

   if __name__ == "__main__":
       asyncio.run(main())
   ```

## Documentation

- [Installation Guide](getting_started/installation.md) - How to install and set up Sifu
- [User Guide](user_guide/core_concepts.md) - Learn about Sifu's core concepts and features
- [API Reference](api_reference/overview.md) - Detailed API documentation
- [Examples](examples/basic_usage.md) - Practical examples and tutorials

## Get Involved

- **GitHub**: [github.com/yourusername/sifu](https://github.com/yourusername/sifu)
- **Issues**: [Report an issue](https://github.com/yourusername/sifu/issues)
- **Discussions**: [Join the discussion](https://github.com/yourusername/sifu/discussions)
- **Contributing**: [Contribution Guide](development/contributing.md)

## License

Sifu is licensed under the [Apache 2.0  License](about/license.md).
