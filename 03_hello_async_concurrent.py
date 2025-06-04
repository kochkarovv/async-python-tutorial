#!/usr/bin/env python3
"""
Concurrent Asynchronous Hello World Example
From: Mastering Python's Asyncio: A Practical Guide by Moraneus

TUTORIAL EXPLANATION:
====================

True Concurrency with asyncio.gather()

This modified version demonstrates the real power of asyncio - running 
multiple tasks concurrently instead of sequentially.

KEY CONCEPTS DEMONSTRATED:
- asyncio.gather(): Runs multiple coroutines concurrently
- Concurrent execution: Tasks run "at the same time"
- Efficient resource utilization during wait times
- Event loop task scheduling and management

HOW CONCURRENT EXECUTION WORKS:
The main() function uses asyncio.gather() to run say_hello_async() and 
do_something_else() concurrently. This means that while the program is 
waiting for the say_hello_async() function to complete its 2-second sleep, 
it starts and potentially completes the do_something_else() function, 
effectively doing another task during the wait time.

THE CHEF ANALOGY IN ACTION:
Now our chef (event loop) starts cooking the stew (hello task), and 
instead of standing idle for 2 seconds, immediately starts prepping 
the salad (another task). The salad finishes in 1 second, then the 
chef waits just 1 more second for the stew to finish.

PERFORMANCE BENEFITS:
- Sequential execution: 2 + 1 = 3 seconds total
- Concurrent execution: max(2, 1) = 2 seconds total
- 33% performance improvement in this example

REAL-WORLD APPLICATIONS:
This pattern is powerful for:
- Multiple API calls
- File I/O operations
- Database queries
- Any I/O-bound operations that can run independently

ASYNCIO.GATHER() BEHAVIOR:
- Starts all tasks simultaneously
- Waits for ALL tasks to complete
- Returns results in the order tasks were passed
- If any task fails, gather() raises the exception
"""

import asyncio
import time

async def say_hello_async():
    """
    First async task - simulates a longer operation
    
    This represents any I/O-bound task that takes time,
    such as an API call or file operation.
    """
    print("Starting hello task...")
    await asyncio.sleep(4)  # Simulates waiting for 4 seconds
    print("Hello, Async World!")

async def do_something_else():
    """
    Second async task that runs concurrently
    
    This demonstrates how other work can happen while
    waiting for the first task to complete.
    """
    print("Starting another task...")
    await asyncio.sleep(2)  # Simulates doing something else for 2 seconds
    print("Finished another task!")

async def main():
    """
    Main function that demonstrates concurrent execution
    
    Uses asyncio.gather() to run multiple coroutines concurrently:
    1. Both tasks start immediately
    2. do_something_else() completes after 2 seconds
    3. say_hello_async() completes after 4 seconds
    4. Total time ≈ 4 seconds (not 6!)
    """
    print("Starting both tasks concurrently...")
    # Schedule both tasks to run concurrently
    await asyncio.gather(
        say_hello_async(),
        do_something_else(),
    )
    print("All tasks completed!")

if __name__ == "__main__":
    print("=== Concurrent Asynchronous Hello World ===")
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print("Notice: Both tasks ran concurrently, so total time ≈ 4 seconds, not 6!") 