from abc import ABC, abstractmethod
import praw
import googleapiclient.discovery
import googleapiclient.errors


class ApiConnector(ABC):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def connect(self, config_file):
        pass


class RedditApiConnector(ApiConnector):
    def __init__(self) -> None:
        super().__init__()

    def connect(self, config_file) -> praw.Reddit:
        try:
            return praw.Reddit(
                client_id=config_file["reddit_use_script"],
                client_secret=config_file["reddit_client_secret"],
                user_agent=config_file["reddit_user_agent"],
                username=config_file["reddit_username"],
                password=config_file["reddit_password"],
            )

        except Exception:
            assert "Could not connect to Reddit. Error: {e}"


class YoutubeApiConnector(ApiConnector):
    def __init__(self) -> None:
        super().__init__()
        self.api_service_name = "youtube"
        self.api_version = "v3"

    def connect(self, config_file) -> googleapiclient.discovery:
        try:
            return googleapiclient.discovery.build(
                self.api_service_name,
                self.api_version,
                developerKey=config_file["youtube_api_key"],
            )

        except Exception:
            assert "Could not connect to Reddit. Error: {e}"
