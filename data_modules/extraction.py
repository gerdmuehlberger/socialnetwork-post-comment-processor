from abc import ABC, abstractmethod
import pandas as pd
import sys
from praw import Reddit
from googleapiclient.discovery import Resource


class DataExtractor(ABC):
    @abstractmethod
    def fetch_raw_comments_dataframe(url: str) -> pd.DataFrame:
        pass


class YoutubeExtractor(DataExtractor):
    def __init__(self, client: Resource):
        super().__init__()
        self.client = client

    def fetch_replies(self, parent_id: str):
        replies = []
        request = self.client.comments().list(
            part="snippet", parentId=parent_id, maxResults=100)
        response = request.execute()

        for item in response.get('items', []):
            reply = item['snippet']
            replies.append([
                reply['likeCount'],
                reply['textDisplay']
            ])
        return replies

    def fetch_raw_comments_dataframe(self, url: str) -> pd.DataFrame:
        try:
            comments = []
            request = self.client.commentThreads().list(
                part="snippet", videoId=url, maxResults=100)
            response = request.execute()

            while True:
                for item in response.get('items', []):
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append([
                        comment['likeCount'],
                        comment['textDisplay']
                    ])

                    if item['snippet']['totalReplyCount'] > 0:
                        replies = self.fetch_replies(
                            item['snippet']['topLevelComment']['id'])
                        comments.extend(replies)

                if 'nextPageToken' in response:
                    request = self.client.commentThreads().list(
                        part="snippet", videoId=url, maxResults=100, pageToken=response['nextPageToken'])
                    response = request.execute()
                else:
                    break

            dataframe = pd.DataFrame(comments, columns=['like_count', 'text'])
            return dataframe

        except Exception as e:
            print("An error occurred: ", e)
            sys.exit()


class RedditExtractor(DataExtractor):
    def __init__(self, client: Reddit) -> None:
        super().__init__()
        self.client = client

    def fetch_raw_comments_dataframe(self, url: str) -> pd.DataFrame:
        try:
            submission = self.client.submission(url=url)
            submissionList = []
            submission.comments.replace_more(limit=None)

            for comment in submission.comments.list():
                submissionList.append([
                    comment.score,
                    comment.body
                ])

            dataframe = pd.DataFrame(
                submissionList, columns=['upvotes', 'text'])
            return dataframe

        except Exception as e:
            print("The URL you entered seems invalid. Please enter a valid Reddit URL.")
            sys.exit()
