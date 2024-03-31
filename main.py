import json
import sys
import os.path
from data_modules import connection
from data_modules import extraction
from utility_modules import utils
from utility_modules import config


cliArguments = utils.parse_cli_arguments()
host = utils.HostParser(cliArguments.url).parse_url()
domain = utils.DomainParser(cliArguments.url).parse_url()


def read_setup_client():
    credential_setup_factories = {
        "reddit": config.RedditCredentialSetup(),
        "youtube": config.YoutubeCredentialSetup()
    }
    return credential_setup_factories[domain]


if os.path.isfile(f'./config/{domain}_config.json'):
    pass
else:
    print(f"Could not find config file for {domain} API client.\n")
    print(f"Please set up your credentials for the {domain} API client first.")
    config_setup_client = read_setup_client()
    config_setup_client.set_credentials()


client_config_file = json.load(open(f'./config/{domain}_config.json'))


def read_url_parser(url) -> utils.URLParser:
    try:
        url_parser_factories = {
            "www.reddit.com": utils.RedditUrlParser(url),
            "www.youtube.com": utils.YoutubeUrlParser(url)
        }
        return url_parser_factories[host]
    except KeyError as e:
        raise e


def read_connector() -> connection.ApiConnector:
    try:
        api_connector_factories = {
            "www.reddit.com": connection.RedditApiConnector(),
            "www.youtube.com": connection.YoutubeApiConnector()
        }
        return api_connector_factories[host]
    except KeyError as e:
        raise e


def read_extractor(client) -> extraction.DataExtractor:
    try:
        data_extractor_factories = {
            "www.reddit.com": extraction.RedditExtractor(client=client),
            "www.youtube.com": extraction.YoutubeExtractor(client=client)
        }
        return data_extractor_factories[host]
    except KeyError as e:
        raise e


def main():
    client = read_connector().connect(config_file=client_config_file)
    url = read_url_parser(cliArguments.url).parse_url()
    raw_dataframe = read_extractor(client).fetch_raw_comments_dataframe(url)

    print(raw_dataframe.head(5))


if __name__ == "__main__":
    main()
