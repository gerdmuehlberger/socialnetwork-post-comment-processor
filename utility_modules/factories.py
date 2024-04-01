from pandas import DataFrame
from data_modules import connection
from data_modules import extraction
from data_modules import transformation
from utility_modules import utils
from utility_modules import config
from utility_modules.constants import HOST, DOMAIN
from utility_modules.sentiment_anal import CachedSentimentProvider, DistillBERTSentimentProvider, RoBERTaSentimentProvider


def get_setup_client() -> config.CredentialsConfigurator:
    credential_setup_factories = {
        "reddit": config.RedditCredentialConfigurator(),
        "youtube": config.YoutubeCredentialConfigurator()
    }
    return credential_setup_factories[DOMAIN]


def get_url_parser() -> utils.URLParser:
    try:
        url_parser_factories = {
            "www.reddit.com": utils.RedditUrlParser(),
            "www.youtube.com": utils.YoutubeUrlParser()
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


def get_sentiment_provider(provider_type: str) -> CachedSentimentProvider:
    if provider_type.lower() == "distillbert":
        return DistillBERTSentimentProvider()
    elif provider_type.lower() == "roberta":
        return RoBERTaSentimentProvider()
    return DistillBERTSentimentProvider()
