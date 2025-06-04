#!/usr/bin/env python3
"""
Basic Asynchronous Hello World Example
From: Mastering Python's Asyncio: A Practical Guide by Moraneus

TUTORIAL EXPLANATION:
====================

Switching Gears to Asyncio - Basic async/await Syntax

Now, let's switch gears to asyncio, showing the asynchronous way.
This example introduces the fundamental async/await pattern.

KEY CONCEPTS DEMONSTRATED:
- async def: Declares an asynchronous function (coroutine)
- await: Pauses execution and yields control back to the event loop
- asyncio.sleep(): Non-blocking alternative to time.sleep()
- asyncio.run(): Entry point for running async code

THE AWAIT RESERVE KEYWORD:
The await keyword in Python is essential for asynchronous programming:
- Context: await can only be used inside async functions
- Purpose: Yields control back to the event loop, suspending execution 
  until the awaited object is resolved
- Non-blocking behavior: What makes asynchronous programming efficient

HOW IT WORKS:
1. async def declares a coroutine function
2. await asyncio.sleep(2) pauses this coroutine for 2 seconds
3. During the pause, the event loop can potentially do other tasks
4. After 2 seconds, execution resumes with the print statement

THE DIFFERENCE FROM SYNCHRONOUS:
With asyncio, while we wait, the event loop can do other tasks, like 
checking emails or playing a tune, making our code non-blocking and 
more efficient. However, in this basic example, we're not yet taking 
advantage of concurrency - that comes in the next example.

AWAITABLES:
Objects that can be used with await must be awaitable:
- Coroutines declared with async def
- asyncio Tasks and Futures
- Any object with an __await__() method
"""

import asyncio
import time

async def say_hello_async():
    """
    Asynchronous version using await
    
    This coroutine demonstrates:
    1. async def syntax for creating coroutines
    2. await for non-blocking waiting
    3. How the event loop manages execution
    """
    print("Starting asynchronous hello...")
    await asyncio.sleep(2)  # Non-blocking operation - yields control to event loop
    print("Hello, Async World!")

if __name__ == "__main__":
    print("=== Basic Asynchronous Hello World ===")
    start_time = time.time()
    # asyncio.run() creates event loop, runs coroutine, and cleans up
    asyncio.run(say_hello_async())
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds") 