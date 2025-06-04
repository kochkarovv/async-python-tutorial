#!/usr/bin/env python3
"""
Synchronous File Reading Example
From: Mastering Python's Asyncio: A Practical Guide by Moraneus

TUTORIAL EXPLANATION:
====================

Reading Files (Concurrent I/O Tasks) - The Synchronous Approach

Let's explore a different use case for demonstrating the benefits of asyncio, 
moving away from web requests to file I/O operations. This can be particularly 
useful when dealing with large files or multiple I/O-bound tasks.

KEY CONCEPTS DEMONSTRATED:
- Sequential file reading operations
- Blocking I/O for file operations
- How I/O wait times add up in synchronous code
- Performance baseline for file operations

THE PROBLEM WITH SYNCHRONOUS FILE READING:
In a synchronous setup, reading multiple files one after the other can 
significantly increase execution time, especially with large files. Even 
with small files, the pattern demonstrates the sequential bottleneck.

SYNCHRONOUS FILE I/O CHARACTERISTICS:
1. Each file is opened, read, and closed before moving to the next
2. Even though file operations are often fast, they still involve I/O
3. For large files or slow storage, the blocking behavior becomes apparent
4. No parallelization of disk operations

WHEN THIS BECOMES A REAL PROBLEM:
- Reading many configuration files at startup
- Processing multiple data files in a batch job
- Loading content from multiple sources
- Working with network-mounted file systems
- Large files that take time to read

THE SEQUENTIAL PATTERN:
file1: open → read → close
file2: open → read → close  
file3: open → read → close

Total time = sum of all individual file operation times

REAL-WORLD SCENARIOS WHERE THIS MATTERS:
- Log file analysis tools processing multiple files
- Data processing pipelines reading from multiple sources
- Configuration managers loading multiple config files
- Document processors handling multiple files
- Backup systems reading multiple directories

This example sets up the comparison baseline. The async version will 
demonstrate how multiple file operations can be performed concurrently, 
which becomes especially beneficial with larger files or slower storage.
"""

import time
import os

def create_sample_files():
    """
    Create sample files for testing
    
    Creates three text files with different content to simulate
    real-world file reading scenarios.
    """
    files_data = {
        'file1.txt': 'This is the content of file 1.\nIt contains some sample text for testing.',
        'file2.txt': 'This is the content of file 2.\nIt has different content than file 1.',
        'file3.txt': 'This is the content of file 3.\nEach file contains unique content for demonstration.'
    }
    
    for filename, content in files_data.items():
        with open(filename, 'w') as f:
            f.write(content)
    
    return list(files_data.keys())

def read_file_sync(filepath):
    """
    Synchronously read a file - blocks during I/O operation
    
    This function demonstrates traditional file I/O:
    1. Open file handle
    2. Read entire contents (blocking operation)
    3. Close file handle
    
    During step 2, the program waits for disk I/O to complete.
    """
    print(f"Starting to read: {filepath}")
    try:
        with open(filepath, 'r') as file:
            content = file.read()  # Blocking I/O operation
        print(f"Completed reading: {filepath}")
        return content
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def read_all_sync(filepaths):
    """
    Read all files synchronously - one after another
    
    Demonstrates the sequential pattern:
    - Process each file completely before starting the next
    - Total time = sum of all individual file read times
    - No parallelization of I/O operations
    """
    results = []
    for filepath in filepaths:
        # Each read_file_sync() call must complete before the next starts
        content = read_file_sync(filepath)
        if content:
            results.append((filepath, content))
    return results

def main():
    """
    Main function demonstrating synchronous file reading
    
    Shows the traditional approach:
    1. Create sample files
    2. Read each file sequentially
    3. Measure total time for comparison with async version
    """
    print("=== Synchronous File Reading ===")
    
    # Create sample files
    filepaths = create_sample_files()
    print(f"Created sample files: {filepaths}")
    
    start_time = time.time()
    
    # Read all files synchronously (one by one)
    results = read_all_sync(filepaths)
    
    end_time = time.time()
    
    print(f"\nResults:")
    for filepath, content in results:
        print(f"  - {filepath}: {len(content)} characters")
        print(f"    Preview: {content[:50]}...")
    
    print(f"\nDone in {end_time - start_time:.4f} seconds")
    print("Notice: Each file was read completely before starting the next")
    
    # Cleanup
    for filepath in filepaths:
        try:
            os.remove(filepath)
        except:
            pass

if __name__ == "__main__":
    main() 