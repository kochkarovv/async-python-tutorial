#!/usr/bin/env python3
"""
Synchronous Hello World Example
From: Mastering Python's Asyncio: A Practical Guide by Moraneus

TUTORIAL EXPLANATION:
====================

"Hello, Async World!" - The Synchronous Approach

Imagine you're tasked with printing "Hello, World!" after a 2-second pause. 
The synchronous approach is straightforward but inefficient.

KEY CONCEPTS DEMONSTRATED:
- Blocking operations: time.sleep(2) causes everything to halt
- Sequential execution: the program waits idle for those 2 seconds
- No concurrency: nothing else can happen during the wait

THE PROBLEM WITH SYNCHRONOUS CODE:
When using time.sleep(2), the entire program comes to a halt while waiting.
This is like having a chef in a kitchen who starts cooking a stew, knows it'll 
take time to simmer, but just stands around doing nothing instead of prepping 
a salad. This blocking behavior is inefficient for I/O-bound operations.

REAL-WORLD IMPACT:
In web applications, this blocking behavior means:
- Server can't handle other requests while waiting
- Poor resource utilization
- Limited scalability
- Bad user experience

This example shows what NOT to do when you need concurrent operations.
The next examples will show how asyncio solves these problems.
"""

import time

def say_hello():
    """
    Synchronous version that blocks execution
    
    This function demonstrates the traditional blocking approach:
    1. Starts a task
    2. Waits (blocks) for completion
    3. Nothing else can happen during this time
    """
    print("Starting synchronous hello...")
    time.sleep(2)  # Blocking operation - everything stops here
    print("Hello, Async World? (not yet)")

if __name__ == "__main__":
    print("=== Synchronous Hello World ===")
    start_time = time.time()
    say_hello()
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds") 