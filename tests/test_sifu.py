"""
Tests for the Sifu system.

This module contains unit and integration tests for the Sifu system.
"""

import pytest
import asyncio
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from sifu import Sifu
from sifu.knowledge import KnowledgeBase, KnowledgeEntry
from sifu.context import ContextManager, Context
from sifu.learning import LearningEngine
from sifu.language import LanguageProcessor
from sifu.matcher import IntentMatcher, Intent, MatchResult
from sifu.api import SifuAPI

# Test data
TEST_KNOWLEDGE = [
    {
        "content": "Sifu is an AI assistant",
        "metadata": {"category": "introduction"},
        "tags": ["ai", "assistant"],
        "language": "en"
    },
    {
        "content": "The weather is usually sunny in California",
        "metadata": {"category": "weather"},
        "tags": ["weather", "california"],
        "language": "en"
    }
]

TEST_INTENTS = [
    {
        "name": "greeting",
        "patterns": ["hello", "hi", "hey"],
        "examples": ["hello there", "hi sifu", "hey there"],
        "description": "Greet the user",
        "confidence_threshold": 0.7,
        "response_templates": ["Hello!", "Hi there!", "Hey! How can I help?"]
    },
    {
        "name": "weather_query",
        "patterns": ["what's the weather", "how's the weather", "weather forecast"],
        "examples": [
            "what's the weather like today?",
            "how's the weather in New York?",
            "weather forecast for tomorrow"
        ],
        "description": "Answer weather-related questions",
        "confidence_threshold": 0.8
    }
]

# Fixtures
@pytest.fixture
def temp_knowledge_file(tmp_path):
    """Create a temporary knowledge file for testing."""
    file_path = tmp_path / "test_knowledge.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(TEST_KNOWLEDGE, f)
    return file_path

@pytest.fixture
def temp_intents_file(tmp_path):
    """Create a temporary intents file for testing."""
    file_path = tmp_path / "test_intents.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({"intents": TEST_INTENTS}, f)
    return file_path

@pytest.fixture
async def knowledge_base(temp_knowledge_file):
    """Create a knowledge base with test data."""
    kb = KnowledgeBase(storage_path=temp_knowledge_file)
    await kb.initialize()
    return kb

@pytest.fixture
def context_manager():
    """Create a context manager for testing."""
    return ContextManager()

@pytest.fixture
def learning_engine():
    """Create a learning engine for testing."""
    return LearningEngine()

@pytest.fixture
def language_processor():
    """Create a language processor for testing."""
    return LanguageProcessor()

@pytest.fixture
def intent_matcher():
    """Create an intent matcher for testing."""
    matcher = IntentMatcher()
    for intent_data in TEST_INTENTS:
        intent = Intent(**intent_data)
        matcher.add_intent(intent)
    return matcher

@pytest.fixture
async def sifu(knowledge_base, context_manager, learning_engine, language_processor, intent_matcher):
    """Create a Sifu instance for testing."""
    sifu = Sifu()
    sifu.knowledge_base = knowledge_base
    sifu.context_manager = context_manager
    sifu.learning_engine = learning_engine
    sifu.language_processor = language_processor
    sifu.intent_matcher = intent_matcher
    return sifu

# Tests
class TestKnowledgeBase:
    """Tests for the KnowledgeBase class."""
    
    async def test_add_entry(self, knowledge_base):
        """Test adding a knowledge entry."""
        entry = await knowledge_base.add_entry(
            content="Test content",
            metadata={"test": "data"},
            tags=["test"],
            language="en"
        )
        
        assert entry.id is not None
        assert entry.content == "Test content"
        assert "test" in entry.tags
        assert entry.language == "en"
        assert entry.confidence == 1.0  # Default confidence
    
    async def test_search(self, knowledge_base):
        """Test searching the knowledge base."""
        # Test exact match
        results = await knowledge_base.search("Sifu is an AI assistant")
        assert len(results) > 0
        assert "Sifu is an AI assistant" in [r.content for r in results]
        
        # Test partial match
        results = await knowledge_base.search("California weather")
        assert len(results) > 0
        assert "sunny in California" in results[0].content
    
    async def test_update_entry(self, knowledge_base):
        """Test updating a knowledge entry."""
        # Add an entry
        entry = await knowledge_base.add_entry("Test content")
        
        # Update the entry
        updated = await knowledge_base.update_entry(
            entry.id,
            content="Updated content",
            metadata={"updated": True},
            tags=["updated"]
        )
        
        assert updated.content == "Updated content"
        assert updated.metadata.get("updated") is True
        assert "updated" in updated.tags
    
    async def test_delete_entry(self, knowledge_base):
        """Test deleting a knowledge entry."""
        # Add an entry
        entry = await knowledge_base.add_entry("Test content")
        
        # Delete the entry
        await knowledge_base.delete_entry(entry.id)
        
        # Verify it's gone
        results = await knowledge_base.search("Test content")
        assert len(results) == 0

class TestContextManager:
    """Tests for the ContextManager class."""
    
    async def test_create_context(self, context_manager):
        """Test creating a new context."""
        context_id = "test_context"
        context = await context_manager.get_or_create_context(context_id)
        
        assert context is not None
        assert context.id == context_id
        assert isinstance(context, Context)
    
    async def test_update_context(self, context_manager):
        """Test updating a context."""
        context_id = "test_context"
        
        # Create a context
        context = await context_manager.get_or_create_context(context_id)
        
        # Add some data
        context.add_entity("name", "Test User")
        context.add_metadata("source", "test")
        
        # Verify updates
        assert context.get_entity("name") == "Test User"
        assert context.get_metadata("source") == "test"
    
    async def test_context_expiration(self, context_manager):
        """Test context expiration."""
        context_id = "temp_context"
        
        # Create a context with a short TTL
        context = await context_manager.get_or_create_context(
            context_id,
            ttl_seconds=1  # 1 second TTL
        )
        
        # Wait for the context to expire
        await asyncio.sleep(1.1)
        
        # Try to get the context (should be expired)
        expired_context = await context_manager.get_context(context_id)
        assert expired_context is None

class TestIntentMatcher:
    """Tests for the IntentMatcher class."""
    
    def test_add_intent(self, intent_matcher):
        """Test adding an intent."""
        # Test that our fixture added the test intents
        intents = intent_matcher.list_intents()
        assert "greeting" in intents
        assert "weather_query" in intents
    
    def test_match_patterns(self, intent_matcher):
        """Test pattern-based intent matching."""
        # Test exact pattern match
        result = intent_matcher.match("hello")
        assert result.intent == "greeting"
        assert result.confidence >= 0.9  # High confidence for exact matches
        
        # Test partial match
        result = intent_matcher.match("hello there")
        assert result.intent == "greeting"
    
    @pytest.mark.skipif(True, reason="ML-based matching requires model download")
    def test_ml_matching(self, intent_matcher):
        """Test ML-based intent matching."""
        # This is a simple test that would require the model to be loaded
        result = intent_matcher.match("what's the weather like today?")
        assert result.intent == "weather_query"
        assert result.confidence >= 0.7  # Should be above threshold

class TestSifuIntegration:
    """Integration tests for the Sifu system."""
    
    async def test_query_processing(self, sifu):
        """Test end-to-end query processing."""
        # Test with a greeting
        response = await sifu.process_query("Hello!")
        assert "text" in response
        assert len(response["text"]) > 0
        
        # Test with a knowledge query
        response = await sifu.process_query("What is Sifu?")
        assert "Sifu is an AI assistant" in response["text"]
    
    async def test_learning_loop(self, sifu):
        """Test the learning loop with feedback."""
        # Initial query
        query = "What's the capital of France?"
        response = await sifu.process_query(query)
        
        # Provide feedback
        feedback = {
            "query": query,
            "response": response,
            "rating": 1,  # Positive feedback
            "better_response": "The capital of France is Paris."
        }
        
        # Record the feedback
        await sifu.learning_engine.record_interaction(
            query=query,
            response=response,
            feedback=feedback
        )
        
        # Verify the knowledge was updated
        results = await sifu.knowledge_base.search("capital of France")
        assert len(results) > 0
        assert any("Paris" in r.content for r in results)

class TestAPI:
    """Tests for the Sifu API."""
    
    async def test_health_check(self, sifu):
        """Test the health check endpoint."""
        api = SifuAPI(sifu)
        response = await api.app.test_client().get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    async def test_query_endpoint(self, sifu):
        """Test the query endpoint."""
        api = SifuAPI(sifu)
        
        # Test with a valid query
        response = await api.app.test_client().post(
            "/query",
            json={"text": "Hello!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert len(data["text"]) > 0
    
    async def test_knowledge_endpoint(self, sifu):
        """Test the knowledge management endpoints."""
        api = SifuAPI(sifu)
        
        # Test adding knowledge
        response = await api.app.test_client().post(
            "/knowledge",
            json={
                "content": "Test API knowledge",
                "metadata": {"source": "test"},
                "tags": ["test"],
                "language": "en"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        
        # Test searching for the added knowledge
        results = await sifu.knowledge_base.search("Test API knowledge")
        assert len(results) > 0
        assert "Test API knowledge" in [r.content for r in results]

# Run tests with: pytest tests/test_sifu.py -v
