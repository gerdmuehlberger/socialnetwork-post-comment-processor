import re
import sys
import requests
import argparse
from urllib.parse import urlparse
from tldextract import extract
from abc import ABC, abstractmethod
from utility_modules import exceptions


def parse_cli_arguments():
    parser = argparse.ArgumentParser(
                        prog='social network post analysing cli tool',
                        description='analyse the mood of users in social media posts',
                        )
    parser.add_argument('--url', type=str, help='URL of the post you want to analyse.')
    # parser.add_argument('--raw_data', type=str, default='false' ,help='Retrieve raw dataset instead of a cleaned one.', choices=['true', 'false'])
    args = parser.parse_args()
    return args


class URLParser(ABC):
    @abstractmethod
    def __init__(self, url) -> None:
        self.url = url
    
    @abstractmethod
    def parse_url() -> str:
        pass


class HostParser(URLParser):
    def __init__(self, url) -> None:
        super().__init__(url)

    def parse_url(self) -> str:
        return urlparse(self.url).netloc


class DomainParser(URLParser):
    def __init__(self, url) -> None:
        super().__init__(url)
    
    def parse_url(self) -> str:
        return extract(self.url).domain


class YoutubeUrlParser(URLParser):
    def __init__(self, url) -> None:
        super().__init__(url)
    
    def parse_url(self) -> str:
        try: 
            # returns video id from youtube url
            return re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", self.url).group(1)
        except Exception as e:
            print("The URL you entered seems invalid. Please enter a valid YouTube URL.")
            sys.exit()


class RedditUrlParser(URLParser):
    def __init__(self, url) -> None:
        super().__init__(url)

    def parse_url(self) -> str:
        response = requests.get(self.url)
        if response.status_code == 200:
            return self.url
        else:
            print("The URL you entered seems invalid. Please enter a valid Reddit URL.")
            sys.exit()
            