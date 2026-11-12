import re
import sys
import argparse
from urllib.parse import urlparse
from tldextract import extract
from praw.exceptions import InvalidURL
from praw.models import Submission
from abc import ABC, abstractmethod


def parse_cli_arguments():
    parser = argparse.ArgumentParser(
        prog="social network post analysing cli tool",
        description="analyse the mood of users in social media posts",
    )
    parser.add_argument("--url", type=str, help="URL of the post you want to analyse.")
    parser.add_argument(
        "--raw_data",
        type=str,
        default="false",
        help="Retrieve raw dataset instead of a cleaned one.",
        choices=["true", "false"],
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path of the file to write the dataset to. The file extension determines the format (e.g. .csv).",
    )
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
        except Exception:
            print(
                "The URL you entered seems invalid. Please enter a valid YouTube URL."
            )
            sys.exit()


class RedditUrlParser(URLParser):
    def __init__(self) -> None:
        super().__init__()

    def parse_url(self, url) -> str:
        try:
            # returns submission id from reddit url
            return Submission.id_from_url(url)
        except InvalidURL:
            print("The URL you entered seems invalid. Please enter a valid Reddit URL.")
            sys.exit()
