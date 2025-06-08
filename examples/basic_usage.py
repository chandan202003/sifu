"""
Basic usage example for the Sifu library.

This script demonstrates how to use the core functionality of Sifu,
including natural language processing, knowledge management, and learning.
"""

import asyncio
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import Sifu components
from sifu import Sifu, knowledge_base, intent_matcher, learning_engine

async def main():
    """Main example function."""
    logger.info("Starting Sifu example...")
    
    # Initialize Sifu
    sifu = Sifu()
    
    # Example 1: Basic query processing
    logger.info("\n=== Example 1: Basic Query Processing ===")
    response = await sifu.process_query("Hello, how are you?")
    print(f"Response: {response}")
    
    # Example 2: Adding knowledge
    logger.info("\n=== Example 2: Adding Knowledge ===")
    await knowledge_base.add_entry(
        content="Sifu is an AI assistant",
        metadata={"category": "introduction"},
        tags=["ai", "assistant"],
        language="en"
    )
    print("Added knowledge entry about Sifu")
    
    # Example 3: Querying knowledge
    logger.info("\n=== Example 3: Querying Knowledge ===")
    results = await knowledge_base.search("What is Sifu?")
    print(f"Knowledge search results: {results}")
    
    # Example 4: Intent matching
    logger.info("\n=== Example 4: Intent Matching ===")
    match = intent_matcher.match("How do I reset my password?")
    print(f"Matched intent: {match.intent} (confidence: {match.confidence:.2f})")
    
    # Example 5: Learning from feedback
    logger.info("\n=== Example 5: Learning from Feedback ===")
    await learning_engine.record_interaction(
        query="What's the weather like?",
        response={"text": "I don't know the current weather."},
        feedback={
            "rating": -1,
            "better_response": "I can check the weather for you. Please enable location services or specify a location."
        }
    )
    print("Recorded feedback for improvement")
    
    # Example 6: Processing a conversation
    logger.info("\n=== Example 6: Processing a Conversation ===")
    conversation = [
        "Hi there!",
        "What can you do?",
        "Tell me about yourself"
    ]
    
    for message in conversation:
        print(f"\nUser: {message}")
        response = await sifu.process_query(message)
        print(f"Sifu: {response.get('text', '')}")
    
    logger.info("Example completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
