import json
from data_modules import connection
from data_modules import extraction
from data_modules import transformation
from utility_modules import utils

# add if condition to check if user has setup credentials here
secrets = json.load(open('./config/secrets.json'))
cliArguments = utils.parseCliArguments()


def read_url_parser(url) -> utils.URLParser:
    url_parser_factories = {
        "reddit": utils.RedditUrlParser(url),
        "youtube": utils.YoutubeUrlParser(url)
    }
    return url_parser_factories[cliArguments.client]


def read_connector() -> connection.ApiConnector:
    api_connector_factories = {
        "reddit": connection.RedditApiConnector(
                                    use_script=secrets['reddit_use_script'],
                                    client_secret=secrets['reddit_client_secret'],
                                    user_agent=secrets['reddit_user_agent'],
                                    username=secrets['reddit_username'],
                                    password=secrets['reddit_password']),
        "youtube": connection.YoutubeApiConnector(api_key=secrets['youtube_api_key'])
    }
    return api_connector_factories[cliArguments.client]


def read_extractor(client) -> extraction.DataExtractor:
    data_extractor_factories = {
        "reddit": extraction.RedditExtractor(client=client),
        "youtube": extraction.YoutubeExtractor(client=client)
    }
    return data_extractor_factories[cliArguments.client]


def main():
    client = read_connector().connect()
    url = read_url_parser(cliArguments.url).parseUrl()
    raw_dataframe = read_extractor(client).fetchRawCommentsDataFrame(url)

    print(raw_dataframe.head(5))


if __name__ == "__main__":
    main()
