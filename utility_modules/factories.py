from utility_modules.constants import HOST, DOMAIN
from data_modules import connection
from data_modules import extraction
from data_modules import transformation
from utility_modules import parsers
from utility_modules import config


def get_setup_client() -> config.CredentialsConfigurator:
    credential_setup_factories = {
        "reddit": config.RedditCredentialConfigurator(),
        "youtube": config.YoutubeCredentialConfigurator()
    }
    return credential_setup_factories[DOMAIN]


def get_url_parser() -> parsers.URLParser:
    try:
        url_parser_factories = {
            "www.reddit.com": parsers.RedditUrlParser(),
            "www.youtube.com": parsers.YoutubeUrlParser()
        }
        return url_parser_factories[HOST]
    except KeyError as e:
        raise e


def get_connector() -> connection.ApiConnector:
    try:
        api_connector_factories = {
            "www.reddit.com": connection.RedditApiConnector(),
            "www.youtube.com": connection.YoutubeApiConnector()
        }
        return api_connector_factories[HOST]
    except KeyError as e:
        raise e


def get_data_cleaner() -> transformation.AbstractDataCleaner:
    try:
        data_transformers = {
            "www.reddit.com": transformation.RedditDataCleaner(),
            "www.youtube.com": transformation.YoutubeDataCleaner()
        }
        return data_transformers[HOST]
    except KeyError as e:
        raise e


def get_extractor(client) -> extraction.DataExtractor:
    try:
        data_extractor_factories = {
            "www.reddit.com": extraction.RedditExtractor(client=client),
            "www.youtube.com": extraction.YoutubeExtractor(client=client)
        }
        return data_extractor_factories[HOST]
    except KeyError as e:
        raise e