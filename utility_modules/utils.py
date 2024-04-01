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
    parser.add_argument('--url', type=str,
                        help='URL of the post you want to analyse.')
    parser.add_argument('--sentiment_provider', type=str,
                        help='Which local sentiment module to use.',
                        default='distillbert')
    parser.add_argument('--raw_data',
                        type=str,
                        default='false',
                        help='Retrieve raw dataset instead of a cleaned one.',
                        choices=['true', 'false'])
    args = parser.parse_args()
    return args


class URLParser(ABC):
    @abstractmethod
    def parse_url(self, url) -> str:
        pass


class HostParser(URLParser):
    def __init__(self) -> None:
        super().__init__()

    def parse_url(self, url) -> str:
        return urlparse(url).netloc


class DomainParser(URLParser):
    def __init__(self) -> None:
        super().__init__()

    def parse_url(self, url) -> str:
        return extract(url).domain


class YoutubeUrlParser(URLParser):
    def __init__(self) -> None:
        super().__init__()

    def parse_url(self, url) -> str:
        try:
            # returns video id from youtube url
            return re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url).group(1)
        except Exception as e:
            print("The URL you entered seems invalid. Please enter a valid YouTube URL.")
            sys.exit()


class RedditUrlParser(URLParser):
    def __init__(self) -> None:
        super().__init__()

    def parse_url(self, url) -> str:
        response = requests.get(url)
        if response.status_code == 200:
            return url
        else:
            print("The URL you entered seems invalid. Please enter a valid Reddit URL. Status code: ",
                  response.status_code)
            sys.exit()
