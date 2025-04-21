import gc

from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError

from ..utils.youtube import extract_video_id
with workflow.unsafe.imports_passed_through():
    from .activities import download, split_audio_by_speaker, tony_voice_detection, transcription, phrase_counting, yt_comment, reddit_post

# Define the Workflow
@workflow.defn
class UnBelievableCountingWorkflow:
    @workflow.run
    async def run(self, youtube_link: str):

        video_id = extract_video_id(youtube_link)
        # Call the activities correctly
        file_path = await workflow.execute_activity(
            download, youtube_link, schedule_to_close_timeout=timedelta(minutes=20), retry_policy=RetryPolicy(maximum_attempts=1)
        )
        if file_path == "":
            raise ApplicationError("File path returned from download is empty")

        splits = await workflow.execute_activity(
            split_audio_by_speaker, file_path, schedule_to_close_timeout=timedelta(hours=3), retry_policy=RetryPolicy(maximum_attempts=1)
        )

        if not splits:
            raise ApplicationError("Splits is None")

        path = await workflow.execute_activity(
            tony_voice_detection, args=(splits, video_id), schedule_to_close_timeout=timedelta(minutes=40), retry_policy=RetryPolicy(maximum_attempts=1)
        )

        if path == "":
            raise ApplicationError("File path returned from tony_voice_detection is empty")

        output_file = await workflow.execute_activity(
            transcription, args=(path, video_id), schedule_to_close_timeout=timedelta(hours=5), retry_policy=RetryPolicy(maximum_attempts=1)
        )

        if output_file == "":
            raise ApplicationError("Output file returned from transcription is empty")

        tony_counts = await workflow.execute_activity(
            phrase_counting, output_file, schedule_to_close_timeout=timedelta(minutes=20), retry_policy=RetryPolicy(maximum_attempts=1)
        )

        if tony_counts == "":
            raise ApplicationError("Tony counts is None")

        comment_youtube_id, episode_name =  await workflow.execute_activity(
            yt_comment, args=(youtube_link, tony_counts), schedule_to_close_timeout=timedelta(hours=4), retry_policy=RetryPolicy(maximum_attempts=1)
        )

        await workflow.execute_activity(
            reddit_post, args=(youtube_link, tony_counts, episode_name), schedule_to_close_timeout=timedelta(hours=4), retry_policy=RetryPolicy(maximum_attempts=1)
        )