import json
import os.path
from utility_modules.constants import CLI_ARGUMENTS, DOMAIN
from utility_modules import factories
from utility_modules.sentiment_anal import SentimentProviderFactory


if os.path.isfile(f'./config/{DOMAIN}_config.json'):
    pass
else:
    print(
        f"\nCould not find config file for {DOMAIN} API client\n\nPlease set \
          up your credentials for the {DOMAIN} API client first\n")

    config_setup_client = factories.get_setup_client()
    config_setup_client.set_credentials()


client_config_file = json.load(open(f'./config/{DOMAIN}_config.json'))


def main():
    client = factories.get_connector().connect(config_file=client_config_file)
    url = factories.get_url_parser().parse_url(CLI_ARGUMENTS.url)
    extractor = factories.get_extractor(client)
    raw_dataframe = extractor.fetch_raw_comments_dataframe(url)
    sentiment_provider = SentimentProviderFactory.get_provider(
        CLI_ARGUMENTS.sentiment_provider
    )
    dataframe_with_sentiment = sentiment_provider.infer_labels_and_scores(
        raw_dataframe
    )

    print(dataframe_with_sentiment.head(5))


if __name__ == "__main__":
    main()
