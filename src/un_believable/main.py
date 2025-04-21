# un_believable/src/un_believable/cli.py
import click
import os
import asyncio
import random
import string

from .utils.config import TEMPORALIO_QUEUE_NAME, TEMPORALIO_WORKFLOW_NAME
from .utils.logger import init as logger

from temporalio.client import Client
from .workflowing.workflows import UnBelievableCountingWorkflow
from .workflowing.worker import start as start_worker

logger = logger()

@click.group()
def main():
    """A poetry project to recognize Tony Hinchcliffe's voice and catchphrases."""
    pass

@main.command()
@click.option('--tony-links-file', type=click.Path(exists=True), help='Path to a file containing YouTube links of Tony Hinchcliffe.')
@click.option('--not-tony-links-file', type=click.Path(exists=True), help='Path to a file containing YouTube links of other speakers.')
def train(tony_links_file, not_tony_links_file):
    """Downloads audio and trains the voice model."""
    # worker_train(tony_links_file, not_tony_links_file)
    logger.info("Disabled intentionally due to a good model training outcome")

@main.command()
def worker():
    """Starts a temporal worker"""
    start_worker()

@main.command()
@click.option('--youtube-link', type=str, required=True, help='The YouTube Short link to analyze.')
def count(youtube_link):
    """Orchestrates a count phrases temporal workflow"""
    async def start_workflow(youtube_link):
        temporalio_address=f"{os.getenv('TEMPORAL_ADDRESS', 'localhost:7233')}"
        client = await Client.connect(temporalio_address)
        
        handle = await client.start_workflow(
            UnBelievableCountingWorkflow.run, 
            youtube_link,
            id=f"{TEMPORALIO_WORKFLOW_NAME}-{''.join(random.choices(string.ascii_letters, k=10))}",
            task_queue=TEMPORALIO_QUEUE_NAME,
        )

        await handle.result()

    asyncio.run(start_workflow(youtube_link))