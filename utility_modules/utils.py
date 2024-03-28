import re
import sys
import requests
import argparse
from utility_modules import exceptions


def parseCliArguments():
    parser = argparse.ArgumentParser(
                        prog='social network post analysing cli tool',
                        description='analyse the mood of users in social media posts',
                        )

    parser.add_argument('--client', type=str, help='Name of the social network you want to retrieve posts from.', choices=['reddit', 'youtube'])
    parser.add_argument('--url', type=str, help='URL of the post you want to analyse.')
    parser.add_argument('--raw_data', type=str, default='false' ,help='Retrieve raw dataset instead of a cleaned one.', choices=['true', 'false'])
    args = parser.parse_args()
    
    return args


class URLParser():
    def __init__(self, url) -> None:
        self.url = url
    
    def parseYoutubeUrl(self):
        try: 
            return re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", self.url).group(1)
        except Exception as e:
            print("The URL you entered seems invalid. Please enter a valid YouTube URL.")
            sys.exit()


    def parseRedditUrl(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return self.url
        else:
            print("The URL you entered seems invalid. Please enter a valid YouTube URL.")
            sys.exit()