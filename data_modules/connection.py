from abc import ABC, abstractmethod
import praw
import googleapiclient.discovery
import googleapiclient.errors
from utility_modules import exceptions


class ApiConnector(ABC):
    @abstractmethod
    def connect(self):
        pass


class RedditApiConnector(ApiConnector):
    def __init__(self, use_script, client_secret, user_agent, username, password) -> None:
        super().__init__()
        self.use_script = use_script
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.username = username
        self.password = password


    def connect(self) -> praw.Reddit:
        try:
            return praw.Reddit(client_id=self.use_script,
                                 client_secret=self.client_secret,
                                 user_agent=self.user_agent,
                                 username=self.username,
                                 password=self.password)

        except Exception as e:
            assert "Could not connect to Reddit. Error: {e}"


class YoutubeApiConnector(ApiConnector):
    def __init__(self, api_key) -> None:
        super().__init__()
        self.api_service_name = 'youtube'
        self.api_version = 'v3'
        self.api_key = api_key


    def connect(self) -> googleapiclient.discovery:
        try:
            return googleapiclient.discovery.build(
                self.api_service_name, self.api_version, developerKey=self.api_key)
        
        except Exception as e:
            assert "Could not connect to Reddit. Error: {e}"
