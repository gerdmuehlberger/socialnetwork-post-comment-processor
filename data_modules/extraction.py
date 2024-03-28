from abc import ABC, abstractmethod
import pandas as pd
import sys
from utility_modules import exceptions


class DataExtractor(ABC):
    @abstractmethod
    def fetchRawCommentsDataFrame(url:str) -> pd.DataFrame:
        pass


class YoutubeExtractor(DataExtractor):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client


    def fetchRawCommentsDataFrame(self, url:str) -> pd.DataFrame:
        try:
            request = self.client.commentThreads().list(
                part = "snippet",
                videoId = url
            )

            response = request.execute()
            comments = []

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append([
                    comment['likeCount'],
                    comment['textDisplay']
                ])

            dataframe = pd.DataFrame(comments, columns=['like_count', 'text'])
            return dataframe
        
        except Exception as e:
            print("The URL you entered seems invalid. Please enter a valid YouTube URL.")
            sys.exit()


class RedditExtractor(DataExtractor):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client


    def fetchRawCommentsDataFrame(self, url:str) -> pd.DataFrame:
        try:
            submission = self.client.submission(url=url)
            submissionList = []
            submission.comments.replace_more(limit=None)

            for comment in submission.comments.list():
                submissionList.append([
                    comment.score,
                    comment.body
                ])

            dataframe = pd.DataFrame(submissionList, columns=['upvotes', 'text'])
            return dataframe
        
        except Exception as e:
            print("The URL you entered seems invalid. Please enter a valid YouTube URL.")
            sys.exit()