# Mastering Python's Asyncio: Practical Examples

This repository contains executable examples from the article "Mastering Python's Asyncio: A Practical Guide" by Moraneus. Each example demonstrates different aspects of asynchronous programming in Python.

## Overview

Python's `asyncio` library enables writing clean, efficient, and scalable code for concurrent I/O operations. This collection of examples progresses from basic concepts to advanced usage patterns.

## Setup

### Prerequisites
- Python 3.7 or higher
- uv package manager (recommended) or pip

### Installation with uv (recommended)
1. Clone or download this repository
2. Install dependencies:
   ```bash
   uv sync
   ```

### Installation with pip
```bash
pip install -r requirements.txt
```

## Examples

### 1. Hello World Examples
- **`01_hello_sync.py`** - Synchronous version showing blocking behavior
- **`02_hello_async_basic.py`** - Basic async/await syntax
- **`03_hello_async_concurrent.py`** - Concurrent execution with asyncio.gather()

**Run them:**
```bash
python 01_hello_sync.py
python 02_hello_async_basic.py
python 03_hello_async_concurrent.py
```

### 2. Web Fetching Examples
- **`04_web_fetching_sync.py`** - Synchronous HTTP requests with requests library
- **`05_web_fetching_async.py`** - Asynchronous HTTP requests with aiohttp

**Run them:**
```bash
python 04_web_fetching_sync.py
python 05_web_fetching_async.py
```

### 3. File Operations Examples
- **`06_file_reading_sync.py`** - Synchronous file reading
- **`07_file_reading_async.py`** - Asynchronous file reading with aiofiles

**Run them:**
```bash
python 06_file_reading_sync.py
python 07_file_reading_async.py
```

### 4. Advanced Examples
- **`08_async_sync_hybrid.py`** - Mixing async and sync code using run_in_executor
- **`09_future_object.py`** - Working with Future objects and callbacks

**Run them:**
```bash
python 08_async_sync_hybrid.py
python 09_future_object.py
```

### 5. FastAPI Background Tasks
- **`10_fastapi_background_tasks.py`** - Simple FastAPI background task execution
- **`test_fastapi_background.py`** - Test client for simple background tasks

**Run the simple background tasks server:**
```bash
python 10_fastapi_background_tasks.py
```

**Test the endpoints (in another terminal):**
```bash
python test_fastapi_background.py
```

**Available endpoints:**
- `POST /start-jobs` - Start two background jobs (3s and 6s)
- `GET /` - API information

### 6. FastAPI File Upload with Background Processing
- **`11_fastapi_file_upload_background.py`** - File upload with background processing
- **`test_file_upload_background.py`** - Test client for file upload

**Run the file upload server:**
```bash
python 11_fastapi_file_upload_background.py
```

**Test file upload (in another terminal):**
```bash
python test_file_upload_background.py
```

**Available endpoints:**
- `POST /upload` - Upload file with background processing
- `GET /uploads` - List uploaded files
- `DELETE /uploads/{filename}` - Delete uploaded file
- `GET /` - API information

### 7. Celery Distributed Task Queue
- **`12_celery_worker_tasks.py`** - Distributed task processing with Celery and Redis
- **`docker-compose.yml`** - Redis setup for Celery message broker
- **Flower** - Web-based monitoring interface for Celery

**Prerequisites:**
```bash
# Install dependencies (including flower)
uv sync

# Start Redis with Docker (on port 6380)
docker-compose up -d

# Verify Redis is running
docker-compose ps
```

**Run Celery worker (in terminal 1):**
```bash
celery -A 12_celery_worker_tasks worker --loglevel=info
```

**Run Flower monitoring (in terminal 2):**
```bash
celery -A 12_celery_worker_tasks flower --port=5555
```

**Run the demo (in terminal 3):**
```bash
python 12_celery_worker_tasks.py
```

**Flower Web Interface:**
- Open http://localhost:5555 in your browser
- Monitor tasks in real-time as they execute
- View worker statistics and performance
- Track task progress and results
- Beautiful dashboard with charts and metrics

**What you'll see:**
- Quick task completes in ~2 seconds
- Slow task hits timeout at 10-15 seconds
- Tasks run in separate worker processes
- Progress monitoring and timeout handling
- Real-time updates in Flower web interface

**Key differences from FastAPI background tasks:**
- Tasks survive application restarts
- Run in separate processes/machines
- Built-in retry and monitoring
- Perfect for heavy computational work

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

## Performance Comparisons

Each synchronous example is paired with its asynchronous counterpart to demonstrate:
- **Execution Time**: Async versions typically complete faster due to concurrency
- **Resource Usage**: Better utilization of I/O wait times
- **Scalability**: Ability to handle multiple operations simultaneously

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

# Concurrent pattern
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

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **Network Timeouts**: Some examples require internet connectivity
3. **File Permissions**: File examples create temporary files in the current directory

### Dependencies
- `aiohttp`: For asynchronous HTTP requests
- `aiofiles`: For asynchronous file operations  
- `requests`: For synchronous HTTP requests (comparison purposes)

## Learning Path

1. Start with basic hello world examples (01-03)
2. Move to I/O operations (04-07)
3. Explore advanced patterns (08-09)
4. Experiment with modifications and extensions

## Next Steps

After completing these examples, consider exploring:
- Web frameworks like FastAPI or aiohttp web server
- Database async drivers (asyncpg, aiomysql)
- Message queues and pub/sub patterns
- Real-time applications with WebSockets

## References

- [Original Article](https://medium.com/@moraneus/mastering-pythons-asyncio-a-practical-guide-0a673265cf04)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [aiofiles Documentation](https://github.com/Tinche/aiofiles)

## License

These examples are for educational purposes. Feel free to use and modify them for learning and development. 