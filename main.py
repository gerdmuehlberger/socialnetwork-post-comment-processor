import json
import os.path
from data_modules import connection
from data_modules import extraction
from utility_modules import utils

if os.path.isfile('./config/secrets.json'):
    print("secrets set up.")
else:
    print("secrets not set up.")

secrets = json.load(open('./config/secrets.json'))
cliArguments = utils.parseCliArguments()
domain = utils.DomainParser(cliArguments.url).getDomain()


def read_url_parser(url) -> utils.URLParser:
    try:
        url_parser_factories = {
            "www.reddit.com": utils.RedditUrlParser(url),
            "www.youtube.com": utils.YoutubeUrlParser(url)
        }
        return url_parser_factories[domain]
    except KeyError as e:
        raise e


def read_connector() -> connection.ApiConnector:
    try:
        api_connector_factories = {
            "www.reddit.com": connection.RedditApiConnector(
                                        use_script=secrets['reddit_use_script'],
                                        client_secret=secrets['reddit_client_secret'],
                                        user_agent=secrets['reddit_user_agent'],
                                        username=secrets['reddit_username'],
                                        password=secrets['reddit_password']),
            "www.youtube.com": connection.YoutubeApiConnector(api_key=secrets['youtube_api_key'])
        }
        return api_connector_factories[domain]
    except KeyError as e:
        raise e


def read_extractor(client) -> extraction.DataExtractor:
    try:
        data_extractor_factories = {
            "www.reddit.com": extraction.RedditExtractor(client=client),
            "www.youtube.com": extraction.YoutubeExtractor(client=client)
        }
        return data_extractor_factories[domain]
    except KeyError as e:
        raise e


def main():
    client = read_connector().connect()
    url = read_url_parser(cliArguments.url).parseUrl()
    raw_dataframe = read_extractor(client).fetchRawCommentsDataFrame(url)

    print(raw_dataframe.head(5))


if __name__ == "__main__":
    main()
