#!/usr/bin/env python3
"""
Asynchronous File Reading Example
From: Mastering Python's Asyncio: A Practical Guide by Moraneus

TUTORIAL EXPLANATION:
====================

Reading Files - The Asynchronous Approach

For the asynchronous version, we use aiofiles, a library that provides support 
for asynchronous file operations. With aiofiles, we can perform file I/O 
operations without blocking the event loop, allowing us to read multiple files 
concurrently.

KEY CONCEPTS DEMONSTRATED:
- aiofiles library for non-blocking file operations
- Concurrent file reading with asyncio.gather()
- async with for proper async resource management
- How async patterns apply beyond just network I/O

THE AIOFILES ADVANTAGE:
If you haven't installed aiofiles yet, you can do so using pip:
pip install aiofiles

With aiofiles, we can perform file I/O operations without blocking the event 
loop, allowing us to read multiple files concurrently.

HOW ASYNC FILE READING WORKS:
1. All file operations start simultaneously
2. While one file is being read from disk, others can start reading
3. I/O operations run concurrently without blocking each other
4. Total time ≈ time of slowest file operation (not sum of all)

PERFORMANCE BENEFITS:
The asynchronous version, by leveraging aiofiles and asyncio.gather, allows 
for concurrent reading of multiple files. This approach significantly reduces 
the total execution time compared to the synchronous version, which reads each 
file one after the other.

WHEN ASYNC FILE I/O MAKES A DIFFERENCE:
- Large files that take time to read
- Many small files (startup configuration loading)
- Network-mounted file systems with latency
- Files on slower storage devices
- Mixed with other I/O operations (network + file)

THE CONCURRENT PATTERN:
file1: open → read → close \
file2: open → read → close  } All happening simultaneously
file3: open → read → close /

Total time ≈ max(file1_time, file2_time, file3_time)

ASYNC WITH FOR FILE OPERATIONS:
The 'async with aiofiles.open()' pattern ensures:
- Proper file handle cleanup
- Exception safety
- Non-blocking file operations
- Resource management in async context

REAL-WORLD APPLICATIONS:
- Configuration managers loading multiple config files
- Log analyzers processing multiple log files
- Data pipelines reading from multiple sources
- Document processors handling batches of files
- Backup systems with concurrent file operations

SCALABILITY BENEFITS:
By performing I/O operations concurrently, we can improve the efficiency of 
programs that need to handle multiple file operations, especially when dealing 
with larger files or slower storage systems.
"""

import asyncio
import aiofiles
import time
import os

def create_sample_files():
    """
    Create sample files for testing async operations
    
    Creates files with different names to distinguish from sync example.
    In real applications, you'd typically work with existing files.
    """
    files_data = {
        'async_file1.txt': 'This is the content of async file 1.\nIt contains some sample text for testing async operations.',
        'async_file2.txt': 'This is the content of async file 2.\nIt demonstrates concurrent file reading capabilities.',
        'async_file3.txt': 'This is the content of async file 3.\nEach file is read asynchronously without blocking others.'
    }
    
    for filename, content in files_data.items():
        with open(filename, 'w') as f:
            f.write(content)
    
    return list(files_data.keys())

async def read_file_async(filepath):
    """
    Asynchronously read a single file using aiofiles
    
    This coroutine demonstrates:
    1. Non-blocking file opening with async with
    2. Asynchronous file reading with await
    3. Proper resource cleanup
    4. Concurrent execution capability
    """
    print(f"Starting to read: {filepath}")
    try:
        # async with ensures proper async file handle management
        async with aiofiles.open(filepath, 'r') as file:
            content = await file.read()  # Non-blocking read operation
        print(f"Completed reading: {filepath}")
        return content
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

async def read_all_async(filepaths):
    """
    Read all files asynchronously and concurrently
    
    This function demonstrates the power of async I/O:
    1. Create tasks for all file operations immediately
    2. All file reads start simultaneously
    3. asyncio.gather() waits for all to complete
    4. Total time ≈ slowest individual file read time
    """
    # Create tasks for all file reading operations - they start immediately!
    tasks = [read_file_async(filepath) for filepath in filepaths]
    
    # Execute all tasks concurrently - this is where concurrency happens
    results = await asyncio.gather(*tasks)
    
    # Pair results with filenames for easier processing
    return [(filepath, content) for filepath, content in zip(filepaths, results) if content]

async def main():
    """
    Main async function demonstrating concurrent file reading
    
    Shows the async pattern:
    1. Create sample files for testing
    2. Start all file reads simultaneously
    3. Wait for all to complete concurrently
    4. Process results after all operations finish
    """
    print("=== Asynchronous File Reading ===")
    
    # Create sample files
    filepaths = create_sample_files()
    print(f"Created sample files: {filepaths}")
    
    start_time = time.time()
    
    # Read all files asynchronously (all at once!)
    results = await read_all_async(filepaths)
    
    end_time = time.time()
    
    print(f"\nResults:")
    for filepath, content in results:
        print(f"  - {filepath}: {len(content)} characters")
        print(f"    Preview: {content[:50]}...")
    
    print(f"\nDone in {end_time - start_time:.4f} seconds")
    print("Notice: Files were read concurrently!")
    print("All file operations started simultaneously, not sequentially!")
    
    # Cleanup
    for filepath in filepaths:
        try:
            os.remove(filepath)
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main()) 