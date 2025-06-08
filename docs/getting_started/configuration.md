# Configuration

Sifu is highly configurable through environment variables and configuration files. This guide explains all available configuration options.

## Configuration Methods

### 1. Environment Variables

Set environment variables in your shell or in a `.env` file in your project root:

```bash
# .env file
DATABASE_URL=sqlite:///sifu.db
LOG_LEVEL=INFO
```

### 2. Configuration File

Create a `config.yaml` or `config.json` file in your project root:

```yaml
# config.yaml
database:
  url: sqlite:///sifu.db
  pool_size: 5
  echo: false

logging:
  level: INFO
  file: logs/sifu.log
  max_size: 10  # MB
  backup_count: 5

server:
  host: 0.0.0.0
  port: 8000
  reload: true
  workers: 1
  log_level: info

nlp:
  model_name: all-MiniLM-L6-v2
  similarity_threshold: 0.7
  max_results: 10

security:
  secret_key: your-secret-key
  algorithm: HS256
  access_token_expire_minutes: 30
```

### 3. Python Configuration

You can also configure Sifu programmatically:

```python
from sifu import Sifu, Settings

settings = Settings(
    database_url="sqlite:///sifu.db",
    log_level="INFO",
    nlp={
        "model_name": "all-MiniLM-L6-v2",
        "similarity_threshold": 0.7
    }
)

sifu = Sifu(settings=settings)
```

## Configuration Options

### Database

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | String | `sqlite:///sifu.db` | Database connection URL |
| `DATABASE_POOL_SIZE` | Integer | `5` | Connection pool size |
| `DATABASE_ECHO` | Boolean | `False` | Echo SQL queries |
| `DATABASE_TIMEOUT` | Integer | `30` | Connection timeout in seconds |

### Server

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `HOST` | String | `0.0.0.0` | Host to bind to |
| `PORT` | Integer | `8000` | Port to listen on |
| `RELOAD` | Boolean | `False` | Enable auto-reload |
| `WORKERS` | Integer | `1` | Number of worker processes |
| `LOG_LEVEL` | String | `info` | Log level (debug, info, warning, error, critical) |
| `CORS_ORIGINS` | List | `["*"]` | Allowed CORS origins |

### NLP

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MODEL_NAME` | String | `all-MiniLM-L6-v2` | Sentence transformer model name |
| `SIMILARITY_THRESHOLD` | Float | `0.7` | Minimum similarity score for matches |
| `MAX_RESULTS` | Integer | `10` | Maximum number of results to return |
| `LANGUAGE` | String | `en` | Default language |

### Security

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SECRET_KEY` | String | Randomly generated | Secret key for JWT tokens |
| `ALGORITHM` | String | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Integer | `30` | Token expiration time in minutes |

### Logging

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `LOG_LEVEL` | String | `INFO` | Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `LOG_FILE` | String | `None` | Log file path |
| `LOG_MAX_SIZE` | Integer | `10` | Max log file size in MB |
| `LOG_BACKUP_COUNT` | Integer | `5` | Number of backup logs to keep |

## Environment Variables Precedence

Configuration is loaded in the following order (later values override earlier ones):

1. Default values
2. Values from `.env` file
3. Environment variables
4. Values from config file
5. Values passed programmatically

## Example Configuration

### Development

```env
# .env
DATABASE_URL=sqlite:///./sifu-dev.db
LOG_LEVEL=DEBUG
RELOAD=true
WORKERS=1
```

### Production

```env
# .env
DATABASE_URL=postgresql://user:password@localhost/sifu
LOG_LEVEL=INFO
RELOAD=false
WORKERS=4
SECRET_KEY=change-this-in-production
```

## Testing Configuration

For testing, you can use a separate configuration:

```python
# tests/conftest.py
import pytest
from sifu import Sifu, Settings

@pytest.fixture
def test_settings():
    return Settings(
        database_url="sqlite:///:memory:",
        log_level="WARNING"
    )

@pytest.fixture
async def sifu(test_settings):
    sifu = Sifu(settings=test_settings)
    await sifu.initialize()
    yield sifu
    await sifu.shutdown()
```

## Advanced Configuration

### Custom Models

You can use custom models by specifying the model path:

```yaml
# config.yaml
nlp:
  model_name: /path/to/your/model
  model_type: sentence-transformers  # or 'spacy', 'huggingface', etc.
```

### Multiple Environments

Use different configuration files for different environments:

```bash
# Load production config
SIFU_CONFIG=config/prod.yaml sifu run

# Load development config
SIFU_CONFIG=config/dev.yaml sifu run
```

### Custom Plugins

Extend Sifu with custom plugins:

```python
# my_plugin.py
from sifu.plugins import Plugin

class MyPlugin(Plugin):
    def on_startup(self, sifu):
        print("My plugin started!")

# config.yaml
plugins:
  - my_plugin.MyPlugin
  - another_plugin.AnotherPlugin
```

## Next Steps

- [User Guide](../user_guide/core_concepts.md) - Learn about Sifu's core concepts
- [API Reference](../api_reference/overview.md) - Detailed API documentation
- [Deployment Guide](../development/deployment.md) - How to deploy Sifu in production
