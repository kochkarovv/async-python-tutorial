#!/usr/bin/env python3
"""
Synchronous Web Page Fetching Example
From: Mastering Python's Asyncio: A Practical Guide by Moraneus

TUTORIAL EXPLANATION:
====================

Fetching Web Pages (Concurrent I/O Tasks) - The Synchronous Approach

Fetching web pages is a classic example to demonstrate the limitations of 
synchronous programming and the power of async programming for I/O-bound tasks.

KEY CONCEPTS DEMONSTRATED:
- Sequential HTTP requests using the requests library
- Blocking I/O operations that waste time
- How network latency compounds in synchronous code
- Performance baseline for comparison with async version

THE PROBLEM WITH SYNCHRONOUS WEB REQUESTS:
This code fetches web pages in a row, one after another. Each request 
blocks until completion before moving to the next. This is inefficient 
because:

1. Network requests involve significant wait time (latency)
2. During each request, the CPU sits idle
3. Total time = sum of all individual request times
4. No parallelization of I/O operations

TYPICAL PERFORMANCE:
- Each HTTP request: ~0.2-0.6 seconds (depending on network)
- 3 sequential requests: ~0.6-1.8 seconds total
- Actual measurement from tutorial: ~0.62 seconds

REAL-WORLD IMPACT:
In applications that need to:
- Fetch data from multiple APIs
- Download multiple files
- Make multiple database queries
- Process multiple user requests

The synchronous approach creates bottlenecks and poor user experience.

WHAT HAPPENS DURING EXECUTION:
1. Send request to example.com → wait → receive response
2. Send request to example.org → wait → receive response  
3. Send request to httpbin.org → wait → receive response

During each "wait", the program does nothing useful - this is where 
asyncio can make a huge difference by utilizing those wait times.

This example sets the baseline. Compare the execution time with the 
async version (05_web_fetching_async.py) to see the dramatic improvement.
"""

import requests
import time

def fetch(url):
    """
    Synchronously fetch a URL - blocks until complete
    
    This function demonstrates the traditional blocking approach:
    1. Send HTTP request
    2. Block/wait for response (network I/O)
    3. Return result
    
    During step 2, the entire program is frozen waiting.
    """
    print(f"Starting to fetch: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Completed fetch: {url} - Status: {response.status_code}")
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    """
    Main function that fetches URLs sequentially
    
    Demonstrates the synchronous pattern:
    - Process each URL one by one
    - Wait for each request to complete before starting the next
    - Total time = sum of all individual request times
    """
    urls = [
        'http://example.com',
        'http://example.org', 
        'http://httpbin.org/get'
    ]
    
    print("=== Synchronous Web Fetching ===")
    start_time = time.time()
    
    results = []
    for url in urls:
        # Each fetch() call blocks until that specific request completes
        result = fetch(url)
        if result:
            results.append(f"Fetched {len(result)} characters from {url}")
    
    end_time = time.time()
    
    print(f"\nResults:")
    for result in results:
        print(f"  - {result}")
    
    print(f"\nDone in {end_time - start_time:.2f} seconds")
    print("Notice: Each request waited for the previous one to complete")

if __name__ == "__main__":
    main() 