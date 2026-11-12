from abc import ABC, abstractmethod
import logging
import sys
import time
import pandas as pd
import praw
import prawcore


class DataExtractor(ABC):
    @abstractmethod
    def fetch_raw_comments_dataframe(self, content_id: str) -> pd.DataFrame:
        pass


class YoutubeExtractor(DataExtractor):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def fetch_raw_comments_dataframe(self, video_id: str) -> pd.DataFrame:
        try:
            request = self.client.commentThreads().list(part="snippet", videoId=video_id)

            response = request.execute()
            comments = []

            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append([comment["likeCount"], comment["textDisplay"]])

            dataframe = pd.DataFrame(comments, columns=["like_count", "text"])
            return dataframe

        except Exception:
            print(
                "The URL you entered seems invalid. Please enter a valid YouTube URL."
            )
            sys.exit()


class RedditRequestProgress(logging.Handler):
    """Prints the number of Reddit API requests made while active.

    prawcore logs one "Fetching: ..." debug record per HTTP request, which is
    the only progress signal replace_more exposes.
    """

    def __init__(self) -> None:
        super().__init__(level=logging.DEBUG)
        self.logger = logging.getLogger("prawcore")
        self.request_count = 0

    def emit(self, record: logging.LogRecord) -> None:
        if str(record.msg).startswith("Fetching:"):
            self.request_count += 1
            print(
                f"\rLoading hidden comments: {self.request_count} requests made",
                end="",
                flush=True,
            )

    def __enter__(self) -> "RedditRequestProgress":
        self.previous_level = self.logger.level
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self)
        return self

    def __exit__(self, *exc_info) -> None:
        self.logger.removeHandler(self)
        self.logger.setLevel(self.previous_level)
        print()


class RedditExtractor(DataExtractor):
    max_retries = 5
    retry_delay_seconds = 5
    retryable_exceptions = (
        prawcore.exceptions.ServerError,
        prawcore.exceptions.RequestException,
        prawcore.exceptions.TooManyRequests,
    )

    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def fetch_raw_comments_dataframe(self, submission_id: str) -> pd.DataFrame:
        submission = self.client.submission(id=submission_id)
        try:
            print(f"Post reports {submission.num_comments} comments, loading all of them")
        except (prawcore.exceptions.NotFound, prawcore.exceptions.Forbidden):
            print("The post could not be found or is not accessible.")
            sys.exit()

        self.load_all_comments(submission)

        submissionList = []
        for comment in submission.comments.list():
            submissionList.append([comment.score, comment.body])

        dataframe = pd.DataFrame(submissionList, columns=["upvotes", "text"])
        return dataframe

    def load_all_comments(self, submission: praw.models.Submission) -> None:
        # replace_more keeps the branches it already expanded, so a retry
        # resumes where the failed attempt stopped instead of starting over
        with RedditRequestProgress():
            for attempt in range(self.max_retries + 1):
                try:
                    submission.comments.replace_more(limit=None)
                    return
                except self.retryable_exceptions as e:
                    if attempt == self.max_retries:
                        raise
                    delay = self.retry_delay_seconds * 2**attempt
                    print(
                        f"\nReddit request failed ({e}), retrying in {delay}s "
                        f"(retry {attempt + 1}/{self.max_retries})"
                    )
                    time.sleep(delay)
