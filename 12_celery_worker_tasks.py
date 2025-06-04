#!/usr/bin/env python3
"""
Celery Distributed Task Queue Example
Advanced Asyncio Tutorial: Chapter 12

TUTORIAL EXPLANATION:
====================

Celery - Distributed Task Queue for Heavy Work

This example demonstrates Celery's distributed task queue system for 
offloading heavy computational work from your main application to 
separate worker processes, even on different machines.

KEY CONCEPTS DEMONSTRATED:
- Celery app configuration with Redis broker
- Task definition with @celery.task decorator
- Synchronous and timeout-based task execution
- Task monitoring and result retrieval
- Worker process separation from main app
- Flower web monitoring interface

THE POWER OF CELERY:
Unlike FastAPI background tasks (same process):
1. Tasks run in separate worker processes/machines
2. Survives application restarts
3. Handles millions of tasks per hour
4. Built-in retry, monitoring, and failure handling
5. Perfect for CPU-intensive or long-running jobs
6. Real-time monitoring with Flower web interface

REAL-WORLD APPLICATIONS:
- Image/video processing
- Machine learning training
- Report generation
- Email campaigns
- Data analysis and ETL jobs

ARCHITECTURE:
Main App → Redis (Broker) → Celery Worker → Task Execution
                ↓
            Flower (Web Monitoring)

FLOWER MONITORING:
Flower provides a beautiful web interface at http://localhost:5555 to monitor:
- Active/processed/failed tasks
- Worker status and statistics
- Task execution times and progress
- Real-time task updates
- Broker connection info
"""

import time
import logging
from datetime import datetime, timedelta
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Celery app configuration
app = Celery(
    '12_celery_worker_tasks',
    broker='redis://localhost:6380/0',  # Redis as message broker
    backend='redis://localhost:6380/0'  # Redis to store task results
)

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Task timeout settings
    task_soft_time_limit=10,  # Soft timeout warning at 10 seconds
    task_time_limit=15,       # Hard timeout kill at 15 seconds
)

@app.task(bind=True)
def quick_calculation(self, numbers: list[int]):
    """
    Quick task that processes numbers (completes in ~2 seconds)
    
    This demonstrates:
    1. Simple task execution within timeout limits
    2. Task metadata and progress tracking
    3. JSON serializable parameters and results
    """
    task_id = self.request.id
    logger.info(f"🟡 Quick task {task_id} started with {len(numbers)} numbers")
    
    start_time = time.time()
    
    # Simulate computation work
    total = 0
    for i, num in enumerate(numbers):
        total += num ** 2  # Simple calculation
        time.sleep(0.1)    # Simulate some work
        
        # Update task progress
        self.update_state(
            state='PROGRESS',
            meta={'current': i + 1, 'total': len(numbers), 'partial_sum': total}
        )
    
    duration = time.time() - start_time
    logger.info(f"🟢 Quick task {task_id} completed in {duration:.1f}s")
    
    return {
        'result': total,
        'duration': duration,
        'processed_numbers': len(numbers),
        'completed_at': datetime.utcnow().isoformat()
    }

@app.task(bind=True)
def slow_calculation(self, iterations: int):
    """
    Slow task that may hit timeout limits (runs for ~12 seconds)
    
    This demonstrates:
    1. Handling soft timeout warnings
    2. Graceful task termination
    3. Exception handling in distributed tasks
    """
    task_id = self.request.id
    logger.info(f"🟡 Slow task {task_id} started with {iterations} iterations")
    
    start_time = time.time()
    result = 0
    
    try:
        for i in range(iterations):
            # Check for soft timeout (warning before hard kill)
            current_time = time.time()
            if current_time - start_time > 9:  # Close to soft limit
                logger.warning(f"⚠️  Task {task_id} approaching timeout limit")
            
            # Heavy computation simulation
            result += sum(j ** 2 for j in range(100))
            time.sleep(0.8)  # Simulate intensive work
            
            # Update progress
            self.update_state(
                state='PROGRESS', 
                meta={'current': i + 1, 'total': iterations, 'elapsed': current_time - start_time}
            )
    
    except SoftTimeLimitExceeded:
        # Handle soft timeout gracefully
        duration = time.time() - start_time
        logger.error(f"🔴 Slow task {task_id} hit soft timeout after {duration:.1f}s")
        
        return {
            'result': result,
            'duration': duration,
            'completed_iterations': i,
            'status': 'timeout_exceeded',
            'message': 'Task exceeded soft time limit'
        }
    
    duration = time.time() - start_time
    logger.info(f"🟢 Slow task {task_id} completed in {duration:.1f}s")
    
    return {
        'result': result,
        'duration': duration,
        'completed_iterations': iterations,
        'status': 'completed',
        'completed_at': datetime.utcnow().isoformat()
    }

# Demo functions
def demo_quick_task():
    """Demo the quick calculation task"""
    print("\n=== Quick Task Demo ===")
    numbers = list(range(1, 21))  # 20 numbers, ~2 seconds
    
    print(f"📤 Sending quick task with {len(numbers)} numbers to worker...")
    task = quick_calculation.delay(numbers)
    
    print(f"📋 Task ID: {task.id}")
    print(f"📊 Task State: {task.state}")
    
    # Wait for result (non-blocking in real apps)
    print("⏳ Waiting for result...")
    result = task.get(timeout=30)  # Wait up to 30 seconds
    
    print(f"✅ Task completed!")
    print(f"📊 Result: {result['result']}")
    print(f"⏱️  Duration: {result['duration']:.1f}s")

def demo_slow_task():
    """Demo the slow calculation task (will likely timeout)"""
    print("\n=== Slow Task Demo (Timeout Test) ===")
    iterations = 15  # Will take ~12 seconds, hitting timeout
    
    print(f"📤 Sending slow task with {iterations} iterations to worker...")
    task = slow_calculation.delay(iterations)
    
    print(f"📋 Task ID: {task.id}")
    print(f"📊 Task State: {task.state}")
    
    # Monitor task progress
    print("⏳ Monitoring task progress...")
    while not task.ready():
        if task.state == 'PROGRESS':
            meta = task.info
            print(f"🔄 Progress: {meta['current']}/{meta['total']} iterations")
        time.sleep(1)
    
    # Get final result
    result = task.get(timeout=30)
    
    print(f"📊 Final Status: {result['status']}")
    print(f"⏱️  Duration: {result['duration']:.1f}s")
    if result['status'] == 'timeout_exceeded':
        print(f"⚠️  Completed only {result['completed_iterations']} iterations")

def main():
    """
    Main demo function
    
    PREREQUISITES:
    1. Start Redis: docker-compose up -d
    2. Start Celery worker: celery -A 12_celery_worker_tasks worker --loglevel=info
    3. Start Flower monitoring: celery -A 12_celery_worker_tasks flower --port=5555
    4. Run this script: python 12_celery_worker_tasks.py
    
    FLOWER WEB INTERFACE:
    - Open http://localhost:5555 in your browser
    - Monitor tasks in real-time
    - View worker statistics
    - Track task execution progress
    """
    print("=== Celery Distributed Task Queue Demo ===")
    print("\nPREREQUISITES:")
    print("1. 🐳 Start Redis: docker-compose up -d")
    print("2. 👷 Start Celery worker: celery -A 12_celery_worker_tasks worker --loglevel=info")
    print("3. 🌸 Start Flower monitoring: celery -A 12_celery_worker_tasks flower --port=5555")
    print("4. 🚀 Run this demo: python 12_celery_worker_tasks.py")
    print("\n🌐 FLOWER WEB INTERFACE:")
    print("   Open http://localhost:5555 in your browser to monitor tasks!")
    
    try:
        # Test connection to Redis
        from redis import Redis
        redis_client = Redis(host='localhost', port=6380, db=0)
        redis_client.ping()
        print("\n✅ Redis connection successful")
        
        # Run demos
        demo_quick_task()
        demo_slow_task()
        
        print("\n💡 TIP: Check Flower web interface to see task execution details!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure Redis and Celery worker are running!")

if __name__ == "__main__":
    main() 