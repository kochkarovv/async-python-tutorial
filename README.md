# Mastering Python's Asyncio: Practical Examples

This repository contains executable examples from the article "Mastering Python's Asyncio: A Practical Guide" by Moraneus. Each example demonstrates different aspects of asynchronous programming in Python.

## Overview

Python's `asyncio` library enables writing clean, efficient, and scalable code for concurrent I/O operations. This collection of examples progresses from basic concepts to advanced usage patterns.

## Setup

### Prerequisites
- Python 3.7 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver

### Quick Start with uv (Recommended)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone or download this repository
cd asyncio_tutorial

# Dependencies are automatically managed by uv
# No manual installation needed!
```

### Alternative Setup with pip
If you prefer using pip:
```bash
pip install -r requirements.txt
```

## Running Examples

### Option 1: Interactive Tutorial (Recommended)
Run all examples in sequence with clear explanations:
```bash
uv run python run_examples.py
```

### Option 2: Individual Examples
Run any specific example using the commands below.

## Examples

### 1. Hello World Examples

**`01_hello_sync.py`** - Synchronous version showing blocking behavior
```bash
uv run python 01_hello_sync.py
```

**`02_hello_async_basic.py`** - Basic async/await syntax
```bash
uv run python 02_hello_async_basic.py
```

**`03_hello_async_concurrent.py`** - Concurrent execution with asyncio.gather()
```bash
uv run python 03_hello_async_concurrent.py
```

**Performance comparison:**
- Sync: ~2 seconds (sequential)
- Async: ~2 seconds (concurrent, but only one task takes 2s)

### 2. Web Fetching Examples

**`04_web_fetching_sync.py`** - Synchronous HTTP requests with requests library
```bash
uv run python 04_web_fetching_sync.py
```

**`05_web_fetching_async.py`** - Asynchronous HTTP requests with aiohttp
```bash
uv run python 05_web_fetching_async.py
```

**Performance comparison:**
- Sync: ~3.36 seconds (sequential requests)
- Async: ~0.89 seconds (concurrent requests) - **4x faster!**

### 3. File Operations Examples

**`06_file_reading_sync.py`** - Synchronous file reading
```bash
uv run python 06_file_reading_sync.py
```

**`07_file_reading_async.py`** - Asynchronous file reading with aiofiles
```bash
uv run python 07_file_reading_async.py
```

**Key difference:** Async version starts reading all files simultaneously

### 4. Advanced Examples

**`08_async_sync_hybrid.py`** - Mixing async and sync code using run_in_executor
```bash
uv run python 08_async_sync_hybrid.py
```

**`09_future_object.py`** - Working with Future objects and callbacks
```bash
uv run python 09_future_object.py
```

## Quick Command Reference

Copy and paste these commands to run examples individually:

```bash
# Hello World Examples
uv run python 01_hello_sync.py              # Synchronous blocking
uv run python 02_hello_async_basic.py       # Basic async/await
uv run python 03_hello_async_concurrent.py  # Concurrent execution

# Web Fetching Examples (great for performance comparison)
uv run python 04_web_fetching_sync.py       # ~3.36 seconds
uv run python 05_web_fetching_async.py      # ~0.89 seconds (4x faster!)

# File Operations Examples
uv run python 06_file_reading_sync.py       # Sequential file reading
uv run python 07_file_reading_async.py      # Concurrent file reading

# Advanced Examples
uv run python 08_async_sync_hybrid.py       # Sync/async integration
uv run python 09_future_object.py           # Future objects and callbacks

# Interactive Tutorial Runner
uv run python run_examples.py               # Run all examples with explanations
```

## Key Concepts Demonstrated

### Core Asyncio Concepts
- **Event Loop**: The central execution device that manages async tasks
- **Coroutines**: Async functions declared with `async def`
- **Tasks**: Scheduled coroutines wrapped in Future objects
- **Futures**: Objects representing eventual results of async operations

### Essential Patterns
- **Concurrent Execution**: Using `asyncio.gather()` to run tasks simultaneously
- **Non-blocking I/O**: Performing file and network operations without blocking
- **Hybrid Approach**: Integrating synchronous code in async applications
- **Error Handling**: Managing exceptions in concurrent environments

## Performance Results (Real Examples)

Based on actual test runs:

| Operation | Synchronous | Asynchronous | Improvement |
|-----------|-------------|--------------|-------------|
| Hello World (concurrent) | 3.0s (if sequential) | 2.0s | 33% faster |
| Web Fetching (3 URLs) | 3.36s | 0.89s | **278% faster** |
| File Reading | <0.001s | 0.002s | Similar (small files) |

## Understanding the Output

When running the examples, pay attention to:
- **Timing**: Compare execution times between sync and async versions
- **Order**: Notice how async tasks can complete out of order
- **Concurrency**: Observe multiple operations starting simultaneously

## Best Practices Demonstrated

1. **Use `async with`** for resource management
2. **Handle exceptions** with try/except blocks
3. **Limit concurrency** when working with external resources
4. **Use appropriate libraries** (aiohttp for HTTP, aiofiles for files)
5. **Integrate legacy code** with run_in_executor

## Common Patterns

### Creating and Running Async Tasks
```python
# Basic pattern
async def main():
    await some_async_function()

asyncio.run(main())

# Concurrent pattern with uv
# uv run python script.py
async def main():
    await asyncio.gather(
        task1(),
        task2(),
        task3()
    )
```

### Error Handling
```python
async def safe_task():
    try:
        result = await risky_operation()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None
```

## Project Structure

```
asyncio_tutorial/
├── 01_hello_sync.py              # Basic sync example
├── 02_hello_async_basic.py       # Basic async example
├── 03_hello_async_concurrent.py  # Concurrent async example
├── 04_web_fetching_sync.py       # Sync web requests
├── 05_web_fetching_async.py      # Async web requests
├── 06_file_reading_sync.py       # Sync file operations
├── 07_file_reading_async.py      # Async file operations
├── 08_async_sync_hybrid.py       # Mixing sync/async
├── 09_future_object.py           # Future objects
├── run_examples.py               # Interactive tutorial runner
├── pyproject.toml                # uv project configuration
├── uv.lock                       # uv lock file
├── requirements.txt              # Pip requirements
└── README.md                     # This file
```

## Why uv?

We recommend `uv` because it:
- **Installs packages 10-100x faster** than pip
- **Automatically manages virtual environments**
- **Resolves dependencies more reliably**
- **Works seamlessly** with existing Python projects
- **No manual venv creation needed**

## Troubleshooting

### Common Issues
1. **Import Errors**: Run with `uv run python script.py` to ensure dependencies are available
2. **Network Timeouts**: Some examples require internet connectivity
3. **File Permissions**: File examples create temporary files in the current directory

### Dependencies
- `aiohttp`: For asynchronous HTTP requests
- `aiofiles`: For asynchronous file operations  
- `requests`: For synchronous HTTP requests (comparison purposes)

## Learning Path

1. **Start with basic examples** (01-03) to understand async/await
2. **Compare performance** with web fetching examples (04-05)
3. **Explore file operations** (06-07) to see concurrent I/O
4. **Master advanced patterns** (08-09) for real-world applications
5. **Use the interactive runner** (`run_examples.py`) for presentations

## Next Steps

After completing these examples, consider exploring:
- **Web frameworks**: FastAPI, aiohttp web server
- **Database drivers**: asyncpg (PostgreSQL), aiomysql (MySQL)
- **Message queues**: aio-pika (RabbitMQ), aiokafka (Kafka)
- **Real-time apps**: WebSockets with aiohttp
- **Testing**: pytest-asyncio for testing async code

## References

- [Original Article](https://medium.com/@moraneus/mastering-pythons-asyncio-a-practical-guide-0a673265cf04)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [uv Documentation](https://docs.astral.sh/uv/)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [aiofiles Documentation](https://github.com/Tinche/aiofiles)

## License

These examples are for educational purposes. Feel free to use and modify them for learning and development. 