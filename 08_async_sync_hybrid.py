#!/usr/bin/env python3
"""
Mixing Async and Sync: Hybrid Approach Example
From: Mastering Python's Asyncio: A Practical Guide by Moraneus

TUTORIAL EXPLANATION:
====================

Mixing Async and Sync: A Hybrid Approach

Sometimes, you can't escape synchronous functions but still want to enjoy the async 
ride. This example demonstrates how to integrate synchronous functions within an 
asynchronous environment using Python's asyncio library.

KEY CONCEPTS DEMONSTRATED:
- loop.run_in_executor(): Running sync code in thread/process pools
- Integration of legacy synchronous code with async applications
- Concurrent execution of mixed sync/async tasks
- Different executor types for different use cases

THE HYBRID APPROACH EXPLAINED:
The provided code demonstrates how to integrate synchronous functions within an 
asynchronous environment using Python's asyncio library.

HOW RUN_IN_EXECUTOR WORKS:
1. The Asynchronous Wrapper (async_wrapper function):
   - This async function demonstrates how to run the synchronous sync_task in a way 
     that does not block the event loop
   - It achieves this by utilizing loop.run_in_executor(None, sync_task)
   - loop.run_in_executor(None, sync_task) schedules sync_task to run in a separate 
     thread or process, depending on the executor used
   - The default executor (None specified as the first argument) runs tasks in a thread pool
   - await is used to wait for the completion of sync_task without blocking the event 
     loop, allowing other asynchronous operations to progress in the meantime

2. Executing Asynchronously (main function):
   - The main async function showcases how to run both synchronous and asynchronous 
     tasks together without blocking
   - asyncio.gather is used to schedule concurrent execution of the async_wrapper and 
     potentially other asynchronous tasks
   - By using gather, you ensure that the event loop can manage multiple tasks, running 
     them concurrently where possible

3. Starting the Event Loop (asyncio.run(main())):
   - Finally, asyncio.run(main()) is called to run the main coroutine, which effectively 
     starts the event loop and executes the tasks scheduled within main

WHY IS THIS APPROACH NEEDED?
- Integration of Legacy Code: In real-world applications, you often encounter legacy 
  code that is synchronous in nature. Rewriting large codebases for async compatibility 
  is not always feasible. This approach allows you to integrate such code into your 
  async applications seamlessly.

- Working with Blocking I/O: Some operations, especially those involving blocking I/O, 
  don't have asynchronous equivalents, or you might be working with third-party libraries 
  that only offer synchronous functions. This technique allows those operations to be 
  offloaded to a thread, freeing the event loop to handle other async tasks.

- CPU-bound Tasks: Although CPU-bound tasks are usually better handled by multiprocessing 
  due to Python's Global Interpreter Lock (GIL), you might sometimes choose to run them 
  in threads for simplicity or because the computational overhead is not excessively high. 
  Using run_in_executor allows these tasks to coexist with I/O-bound asynchronous tasks.

EXECUTOR TYPES:
- ThreadPoolExecutor: Good for I/O-bound synchronous tasks
- ProcessPoolExecutor: Better for CPU-bound tasks (bypasses GIL)
- None (default): Uses the default ThreadPoolExecutor
"""

import asyncio
import time

def sync_task(name, duration):
    """
    A synchronous task that simulates blocking work
    
    This represents legacy code or third-party libraries that
    only provide synchronous interfaces.
    """
    print(f"Starting slow sync task '{name}'...")
    time.sleep(duration)  # Simulating a long, blocking task
    print(f"Finished sync task '{name}' after {duration} seconds.")
    return f"Result from {name}"

def cpu_intensive_task(n):
    """
    A CPU-intensive synchronous task
    
    This type of task benefits from ProcessPoolExecutor
    to bypass Python's GIL limitations.
    """
    print(f"Starting CPU-intensive task with n={n}")
    result = sum(i * i for i in range(n))
    print(f"CPU-intensive task completed: sum of squares up to {n}")
    return result

async def async_wrapper(name, duration):
    """
    Async wrapper that runs sync tasks without blocking the event loop
    
    This demonstrates the key pattern:
    1. Get the running event loop
    2. Use run_in_executor to run sync code in a thread
    3. await the result without blocking other async tasks
    """
    loop = asyncio.get_running_loop()
    # Run the synchronous task in a thread pool
    result = await loop.run_in_executor(None, sync_task, name, duration)
    return result

async def async_task(name, duration):
    """
    A regular async task for comparison
    
    Shows how pure async tasks work alongside
    wrapped synchronous tasks.
    """
    print(f"Starting async task '{name}'...")
    await asyncio.sleep(duration)
    print(f"Finished async task '{name}' after {duration} seconds.")
    return f"Async result from {name}"

async def cpu_wrapper(n):
    """
    Async wrapper for CPU-intensive tasks
    
    For CPU-bound work, consider using ProcessPoolExecutor
    instead of the default ThreadPoolExecutor.
    """
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, cpu_intensive_task, n)
    return result

async def main():
    """
    Main function demonstrating the hybrid approach
    
    Shows how to mix sync and async tasks:
    1. Wrap sync tasks with run_in_executor
    2. Use asyncio.gather to run everything concurrently
    3. Both sync and async tasks complete efficiently
    """
    print("=== Mixing Async and Sync: Hybrid Approach ===")
    
    start_time = time.time()
    
    # Mix async and sync tasks running concurrently
    results = await asyncio.gather(
        async_wrapper("Sync-1", 2),        # Sync task wrapped in async
        async_task("Async-1", 1),          # Pure async task
        async_wrapper("Sync-2", 3),        # Another sync task wrapped
        async_task("Async-2", 1.5),        # Another pure async task
        cpu_wrapper(100000),               # CPU-intensive task
        return_exceptions=True
    )
    
    end_time = time.time()
    
    print(f"\nResults:")
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  Task {i+1}: Error - {result}")
        else:
            print(f"  Task {i+1}: {result}")
    
    print(f"\nTotal time: {end_time - start_time:.2f} seconds")
    print("Notice: Sync tasks ran in thread pool without blocking async tasks!")

async def demonstrate_executor_types():
    """
    Demonstrate different executor types
    
    Shows the difference between ThreadPoolExecutor and
    ProcessPoolExecutor for different types of workloads.
    """
    print("\n=== Different Executor Types ===")
    
    import concurrent.futures
    
    loop = asyncio.get_running_loop()
    
    # Using ThreadPoolExecutor (default) - good for I/O-bound tasks
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as thread_executor:
        thread_result = await loop.run_in_executor(
            thread_executor, 
            sync_task, 
            "Thread", 
            1
        )
        print(f"Thread executor result: {thread_result}")
    
    # Using ProcessPoolExecutor for CPU-bound tasks - bypasses GIL
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as process_executor:
        process_result = await loop.run_in_executor(
            process_executor, 
            cpu_intensive_task, 
            500000
        )
        print(f"Process executor result: {process_result}")

if __name__ == "__main__":
    asyncio.run(main())
    
    print("\nPress Enter to see different executor types demonstration...")
    input()
    
    asyncio.run(demonstrate_executor_types()) 