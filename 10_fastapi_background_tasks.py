#!/usr/bin/env python3
"""
FastAPI Background Tasks Example - Simplified Version
Advanced Asyncio Tutorial: Chapter 10

TUTORIAL EXPLANATION:
====================

FastAPI Background Tasks - Simple Non-blocking Execution

This simplified example demonstrates FastAPI's background tasks feature with
basic synchronous operations. The key concept is that HTTP responses return
immediately while background jobs run after the response is sent.

KEY CONCEPTS DEMONSTRATED:
- FastAPI BackgroundTasks: Non-blocking task execution
- Response-first pattern: Return HTTP response immediately  
- Multiple background jobs from single endpoint
- Synchronous operations in background (time.sleep)
- Simple logging to show task execution timing

THE POWER OF BACKGROUND TASKS:
When you call the endpoint:
1. HTTP response returns immediately (~5-10ms)
2. Two background jobs start after response is sent
3. Job 1: Runs for 3 seconds, then logs completion
4. Job 2: Runs for 6 seconds, then logs completion
5. User doesn't wait for the jobs to complete

REAL-WORLD APPLICATIONS:
- Send email notifications
- Process uploaded files
- Update databases
- Generate reports
- Clean up temporary data

PERFORMANCE BENEFIT:
- User gets instant feedback
- Heavy work happens in background
- API stays responsive under load
"""

import logging
import os
import time
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, UploadFile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# FastAPI app instance
app = FastAPI(title="Simple Background Tasks Tutorial", version="1.0.0")

# Background task functions (using synchronous time.sleep)
async def save_files_task(file_data_list: list[tuple[str, bytes]], folder: str) -> None:
    """
    Background task to save files to disk
    
    Args:
        file_data_list: List of tuples containing (filename, file_content)
        folder: Target folder to save files
    """
    os.makedirs(folder, exist_ok=True)

    for filename, file_content in file_data_list:
        file_path = os.path.join(folder, filename)
        
        with open(file_path, "wb") as f:
            f.write(file_content)
            logger.info(f"✅ File {file_path} has been written.")


@app.post("/upload")
async def post_upload_files(files: list[UploadFile], background_tasks: BackgroundTasks):
    """
    Upload multiple files with background processing
    
    This endpoint demonstrates:
    1. Reading file content immediately in the request handler
    2. Passing file content (not file objects) to background task
    3. Immediate response while file writing happens in background
    """
    # Read all file contents immediately (before background task)
    file_data_list = []
    for file in files:
        content = await file.read()
        file_data_list.append((file.filename, content))
    
    # Add background task with file content (not file objects)
    background_tasks.add_task(
        save_files_task,
        file_data_list,
        "data"
    )

    logger.info(f"📤 Returning immediate response for {len(files)} files")
    return {
        "message": f"{len(files)} files are being processed and saved in background",
        "files": [file.filename for file in files],
        "note": "Files are being written to 'data' folder in background",
        "current_time": datetime.now().isoformat()
    }

def background_job_short():
    """
    Background job that takes 3 seconds
    
    This demonstrates:
    1. Synchronous operation in background
    2. Simple timing with time.sleep()
    3. Logging when job completes
    """
    logger.info("🟡 Short job started (3 seconds)")
    time.sleep(3)  # Simulate 3 seconds of work
    logger.info("🟢 Short job completed after 3 seconds!")

def background_job_long():
    """
    Background job that takes 6 seconds
    
    This demonstrates:
    1. Longer synchronous operation
    2. Multiple jobs can run simultaneously 
    3. Jobs complete independently
    """
    logger.info("🟡 Long job started (6 seconds)")
    time.sleep(6)  # Simulate 6 seconds of work
    logger.info("🟢 Long job completed after 6 seconds!")

# Single API endpoint

@app.post("/start-jobs")
def start_background_jobs(background_tasks: BackgroundTasks):
    """
    Single endpoint that starts two background jobs
    
    This endpoint demonstrates:
    1. Adding multiple background tasks
    2. Immediate response while jobs run
    3. Jobs start after HTTP response is sent
    4. Simple, clean background task pattern
    """
    start_time = datetime.now()
    
    # Add both background tasks
    background_tasks.add_task(background_job_short)
    background_tasks.add_task(background_job_long)
    
    logger.info("📤 HTTP response being sent immediately")
    
    # Return immediate response
    return {
        "message": "Two background jobs started!",
        "job_1": "Will complete in 3 seconds",
        "job_2": "Will complete in 6 seconds", 
        "started_at": start_time.isoformat(),
        "note": "Check server logs to see job completion"
    }

@app.get("/")
def root():
    """Root endpoint with instructions"""
    return {
        "message": "Simple FastAPI Background Tasks Demo",
        "instruction": "POST to /start-jobs to see background tasks in action",
        "how_it_works": [
            "1. POST request returns immediately",
            "2. Two background jobs start after response",
            "3. Job 1 completes in 3 seconds",
            "4. Job 2 completes in 6 seconds",
            "5. Check server logs for completion messages"
        ]
    }

# Demo function
def demo_explanation():
    """
    Explanation of what happens when you test this
    """
    print("=== FastAPI Background Tasks Demo ===")
    print("When you POST to /start-jobs:")
    print("1. ⚡ HTTP response returns instantly (~5ms)")
    print("2. 🟡 Background jobs start after response sent")
    print("3. 🟢 Short job finishes in 3 seconds")
    print("4. 🟢 Long job finishes in 6 seconds")
    print("5. 📋 Check server logs for timing details")

if __name__ == "__main__":
    import uvicorn
    print("\n=== Simple FastAPI Background Tasks Server ===")
    print("Server starting on http://localhost:8910")
    print("Test endpoint: POST /start-jobs")
    print("Info endpoint: GET /")
    print("\nPress Ctrl+C to stop")
    
    demo_explanation()
    
    # Run the FastAPI server
    uvicorn.run(app, host="127.0.0.1", port=8910) 