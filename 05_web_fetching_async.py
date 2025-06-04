#!/usr/bin/env python3
"""
Asynchronous Web Page Fetching Example
From: Mastering Python's Asyncio: A Practical Guide by Moraneus

TUTORIAL EXPLANATION:
====================

Fetching Web Pages - The Asynchronous Approach

This example demonstrates the dramatic performance improvement when using 
aiohttp and asyncio for concurrent HTTP requests instead of sequential ones.

KEY CONCEPTS DEMONSTRATED:
- aiohttp.ClientSession: Async HTTP client with connection pooling
- async with: Proper resource management for async operations
- asyncio.gather(*tasks): Concurrent execution of multiple HTTP requests
- Massive performance improvements for I/O-bound operations

THE POWER OF ASYNC WEB REQUESTS:
Let's amp up the efficiency with aiohttp and asyncio! This async version 
doesn't wait around. While one page is being fetched, it starts on the 
next, drastically cutting down total wait time.

PERFORMANCE COMPARISON FROM THE TUTORIAL:
- Synchronous version: ~0.62 seconds (requests one by one)
- Asynchronous version: ~0.30 seconds (requests concurrently) 
- Improvement: ~2x faster with just 3 URLs!

HOW CONCURRENT FETCHING WORKS:
1. All HTTP requests start simultaneously
2. While waiting for response from example.com, also waiting for example.org
3. All network I/O happens in parallel
4. Total time ≈ time of slowest request (not sum of all requests)

THE AIOHTTP ADVANTAGE:
- Built specifically for asyncio
- Connection pooling and reuse
- Non-blocking I/O operations
- Proper resource management with async context managers

ASYNC WITH STATEMENT:
The 'async with' statement ensures proper resource cleanup:
- Automatically closes connections when done
- Handles exceptions gracefully
- Prevents resource leaks in long-running applications

REAL-WORLD IMPACT:
This pattern is incredibly powerful for:
- Microservices making multiple API calls
- Web scrapers fetching many pages
- Data pipelines aggregating from multiple sources
- Any application dealing with multiple I/O operations

SCALABILITY BENEFITS:
- Can handle hundreds or thousands of concurrent requests
- Memory-efficient compared to threading
- No need for complex thread synchronization
- Better resource utilization

The dramatic performance difference makes this a must-use pattern 
for any I/O-bound Python application.
"""

import aiohttp
import asyncio
import time

async def fetch_async(url, session):
    """
    Asynchronously fetch a URL using aiohttp
    
    This coroutine demonstrates:
    1. Non-blocking HTTP request
    2. Proper async resource management with 'async with'
    3. Concurrent execution capability
    4. Exception handling in async context
    """
    print(f"Starting to fetch: {url}")
    try:
        # async with ensures proper connection cleanup
        async with session.get(url, timeout=10) as response:
            content = await response.text()
            print(f"Completed fetch: {url} - Status: {response.status}")
            return content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def main():
    """
    Main async function demonstrating concurrent HTTP requests
    
    Pattern used:
    1. Create aiohttp.ClientSession for connection pooling
    2. Create list of tasks for all URLs
    3. Use asyncio.gather() to run all requests concurrently
    4. Process results after all complete
    
    Key insight: All requests start immediately, run in parallel,
    and complete in approximately the time of the slowest request.
    """
    urls = [
        'http://example.com',
        'http://example.org',
        'http://httpbin.org/get'
    ]
    
    print("=== Asynchronous Web Fetching ===")
    start_time = time.time()
    
    # async with ensures session is properly closed
    async with aiohttp.ClientSession() as session:
        # Create tasks for all URLs - they start immediately
        tasks = [fetch_async(url, session) for url in urls]
        
        # Run all tasks concurrently - this is where the magic happens!
        results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    
    print(f"\nResults:")
    for i, result in enumerate(results):
        if result:
            print(f"  - Fetched {len(result)} characters from {urls[i]}")
    
    print(f"\nDone in {end_time - start_time:.2f} seconds")
    print("Notice: Much faster than synchronous version!")
    print("All requests ran concurrently, not sequentially!")

if __name__ == "__main__":
    asyncio.run(main()) 