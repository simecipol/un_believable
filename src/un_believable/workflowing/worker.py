import asyncio
import os
import time
import psutil
import threading

from temporalio.client import Client
from temporalio.worker import Worker
from .workflows import UnBelievableCountingWorkflow, download, split_audio_by_speaker, tony_voice_detection, transcription, phrase_counting, yt_comment, reddit_post
from ..utils.config import TEMPORALIO_QUEUE_NAME

async def run_worker():
    process = psutil.Process(os.getpid())
    def print_memory_usage():
        """Function to print memory usage every 0.5 seconds."""
        process = psutil.Process(os.getpid())
        while True:
            mem_info = process.memory_info()
            memory_usage = mem_info.rss / (1024 * 1024)  # Convert to MB
            print(f"Memory Usage: {memory_usage:.2f} MB")
            time.sleep(1)

    monitor_thread = threading.Thread(target=print_memory_usage, daemon=True)
    monitor_thread.start()

    temporalio_address=f"{os.getenv('TEMPORAL_ADDRESS', 'localhost:7233')}"
    print(f"Starting worker on {temporalio_address}")
    client = await Client.connect(f"{temporalio_address}")

    worker = Worker(
        client,
        task_queue=TEMPORALIO_QUEUE_NAME,  # Task queue must match workflow's queue
        workflows=[UnBelievableCountingWorkflow],  
        activities=[
            download, 
            split_audio_by_speaker, 
            tony_voice_detection,
            transcription, 
            phrase_counting,
            yt_comment,
            reddit_post,            
        ],
        max_cached_workflows=0
    )

    print("Worker started...")
    await worker.run()  # This runs indefinitely

def start():
    asyncio.run(run_worker())
