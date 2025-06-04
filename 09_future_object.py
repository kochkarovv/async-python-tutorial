#!/usr/bin/env python3
"""
The Future() Object Example
From: Mastering Python's Asyncio: A Practical Guide by Moraneus

TUTORIAL EXPLANATION:
====================

The Future() Object

In Python's asynchronous programming model, a Future is a low-level awaitable 
object that represents an eventual result of an asynchronous operation. When you 
create a Future, you're essentially declaring a placeholder for a result that will 
be available at some point in the future. Futures are a crucial part of the asyncio 
library, allowing for fine-grained control over asynchronous operations.

UNDERSTANDING FUTURES:
• Role: Futures are used to bridge low-level asynchronous operations with high-level 
  asyncio applications. They provide a way to manage the state of an asynchronous 
  operation: pending, finished (with a result), or failed (with an exception).

• Usage: Typically, you don't need to create Futures yourself when using high-level 
  asyncio functions and constructs (like Tasks, which are a subclass of Future). 
  However, understanding Futures is essential for interfacing with lower-level 
  async APIs or when building complex asynchronous systems.

WORKING WITH FUTURES:
A Future object has several key methods and properties:

• set_result(result): Sets the result of the Future. This will mark it as done and 
  notify all awaiting coroutines.

• set_exception(exception): Sets an exception as the result of the Future. This also 
  marks it as done but will raise the exception when awaited.

• add_done_callback(callback): Adds a callback function to be called when the 
  Future is done (either completed with a result or an exception).

• result(): Returns the result of the Future. If the Future is not done, it will raise 
  an InvalidStateError. If the Future is completed with an exception, this method 
  will re-raise the exception.

• done(): Returns True if the Future is done. A Future is considered done if it has 
  a result or an exception.

HOW IT WORKS:
• async_operation is an async function simulating an asynchronous task that takes 
  a Future object and some data as arguments. It waits for 1 second to mimic some 
  async work. Based on the data value, it either sets a result on the Future using 
  set_result or raises an exception using set_exception.

• future_callback is a callback function that prints the result of the Future once 
  it's done. It checks if the operation succeeded or failed by calling future.result(), 
  which either returns the result or re-raises the exception set in the Future.

• In the main coroutine, a Future object is created, and future_callback is added 
  as its callback using add_done_callback. The async_operation is then awaited with 
  the Future and sample data ("success" or any other value to simulate failure).

• After async_operation completed, main check if the Future is done using done(). 
  It then attempts to print the result directly, handling any potential exceptions.

This example succinctly demonstrates the basic mechanisms of managing asynchronous 
operations with Futures in Python's asyncio, including setting results, handling 
exceptions, using callbacks, and retrieving operation outcomes.

PRACTICAL APPLICATIONS:
- Building custom async libraries
- Interfacing with callback-based APIs
- Fine-grained control over async operations
- Creating async primitives and synchronization tools
"""

import asyncio
import random

# A function to simulate an asynchronous operation using a Future
async def async_operation(future, data, delay=3):
    """
    Simulate an async operation that sets a Future's result
    
    This function demonstrates how to manually control a Future:
    1. Perform some async work (simulated with sleep)
    2. Set either a result or exception based on input
    3. The Future becomes "done" and notifies any callbacks
    """
    await asyncio.sleep(delay)  # Simulate some async work with a delay
    
    # Set the result or exception based on the input data
    if data == "success":
        future.set_result("Operation succeeded")
    elif data == "error":
        future.set_exception(RuntimeError("Operation failed"))
    else:
        future.set_result(f"Operation completed with data: {data}")

# A callback function to be called when the Future is done
def future_callback(future):
    """
    Callback function executed when Future completes
    
    This demonstrates the callback pattern:
    1. Automatically called when Future is done
    2. Can access the result or exception
    3. Useful for cleanup or notification tasks
    """
    try:
        result = future.result()  # Attempt to get the result
        print(f"Callback executed - Result: {result}")
    except Exception as exc:
        print(f"Callback executed - Exception: {exc}")

async def basic_future_example():
    """
    Basic example of Future usage
    
    Shows the fundamental Future pattern:
    1. Create a Future object
    2. Add callbacks for when it completes
    3. Start async operation that will set the result
    4. Check the result when done
    """
    print("=== Basic Future Example ===")
    
    # Create a Future object
    future = asyncio.Future()
    
    # Add a callback to the Future
    future.add_done_callback(future_callback)
    
    # Start the asynchronous operation and pass the Future
    print("Starting async operation...")
    await async_operation(future, "success")  # Try changing "success" to "error"
    
    # Check if the Future is done and print its result
    if future.done():
        try:
            result = future.result()
            print(f"Main thread - Result: {result}")
        except Exception as exc:
            print(f"Main thread - Exception: {exc}")

async def multiple_futures_example():
    """
    Example with multiple Futures
    
    Demonstrates managing multiple concurrent operations
    using separate Future objects for each.
    """
    print("\n=== Multiple Futures Example ===")
    
    # Create multiple futures
    futures = []
    operations = [
        ("success", 2),
        ("custom_data", 4), 
        ("error", 1),
        ("another_success", 7)
    ]
    
    for i, (data, delay) in enumerate(operations):
        future = asyncio.Future()
        future.add_done_callback(lambda f, idx=i: print(f"Future {idx} callback executed"))
        futures.append(future)
        
        # Start async operation (don't await yet)
        asyncio.create_task(async_operation(future, data, delay))
    
    print("All operations started...")
    
    # Wait for all futures to complete
    for i, future in enumerate(futures):
        try:
            result = await future
            print(f"Future {i}: {result}")
        except Exception as e:
            print(f"Future {i} failed: {e}")

async def future_with_timeout_example():
    """
    Example showing Future with timeout
    
    Demonstrates how to handle slow operations
    by setting timeouts on Future objects.
    """
    print("\n=== Future with Timeout Example ===")
    
    future = asyncio.Future()
    
    # Start a slow operation
    slow_task = asyncio.create_task(async_operation(future, "slow_result", 6))
    
    try:
        # Wait for the future with a timeout
        result = await asyncio.wait_for(future, timeout=3.0)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out!")
        slow_task.cancel()  # Cancel the slow task

async def future_state_monitoring():
    """
    Example showing Future state monitoring
    
    Shows how to check Future state and monitor
    its progress until completion.
    """
    print("\n=== Future State Monitoring ===")
    
    future = asyncio.Future()
    
    print(f"Future done: {future.done()}")
    print(f"Future cancelled: {future.cancelled()}")
    
    # Set result after a delay
    asyncio.create_task(async_operation(future, "monitored_result", 1))
    
    # Monitor the future state
    while not future.done():
        print("Future still pending...")
        await asyncio.sleep(0.3)
    
    print(f"Future done: {future.done()}")
    print(f"Result: {future.result()}")

async def cancellation_example():
    """
    Example showing Future cancellation
    
    Demonstrates how to cancel ongoing operations
    and handle cancellation properly.
    """
    print("\n=== Future Cancellation Example ===")
    
    future = asyncio.Future()
    
    # Start an operation
    task = asyncio.create_task(async_operation(future, "will_be_cancelled", 3))
    
    # Wait a bit then cancel
    await asyncio.sleep(1)
    
    if not future.done():
        print("Cancelling the future...")
        task.cancel()
        
        try:
            await future
        except asyncio.CancelledError:
            print("Future was cancelled")

async def manual_future_control():
    """
    Example of manually controlling a Future
    
    Shows how to directly set results or exceptions
    on Future objects for custom control flow.
    """
    print("\n=== Manual Future Control ===")
    
    future = asyncio.Future()
    
    # Randomly decide success or failure
    if random.choice([True, False]):
        print("Setting successful result...")
        future.set_result("Manually set success!")
    else:
        print("Setting exception...")
        future.set_exception(ValueError("Manually set error!"))
    
    try:
        result = await future
        print(f"Manual result: {result}")
    except Exception as e:
        print(f"Manual exception: {e}")

async def main():
    """Main function running all examples"""
    await basic_future_example()
    
    print("\nPress Enter to continue to the next example...")
    input()
    
    await multiple_futures_example()
    
    print("\nPress Enter to continue to the next example...")
    input()
    
    await future_with_timeout_example()
    
    print("\nPress Enter to continue to the next example...")
    input()
    
    await future_state_monitoring()
    
    print("\nPress Enter to continue to the next example...")
    input()
    
    await cancellation_example()
    
    print("\nPress Enter to continue to the next example...")
    input()
    
    await manual_future_control()
    
    print("\n🎉 All Future examples completed!")
    print("\nKey takeaways:")
    print("• Futures represent eventual results of async operations")
    print("• Callbacks execute when Futures complete")
    print("• Futures can be cancelled or time out")
    print("• Manual control allows custom async patterns")
    print("• Understanding Futures helps with advanced asyncio usage")

if __name__ == "__main__":
    asyncio.run(main()) 