import json
import os.path
from utility_modules.constants import cliArguments, domain
from utility_modules import factories


if os.path.isfile(f'./config/{domain}_config.json'):
    pass
else:
    print(f"\nCould not find config file for {domain} API client\n\nPlease set up your credentials for the {domain} API client first\n")

    config_setup_client = factories.get_setup_client()
    config_setup_client.set_credentials()

client_config_file = json.load(open(f'./config/{domain}_config.json'))


def main():
    client = factories.get_connector().connect(config_file=client_config_file)
    url = factories.get_url_parser().parse_url(cliArguments.url)
    raw_dataframe = factories.get_extractor(client).fetch_raw_comments_dataframe(url)

    print(raw_dataframe.head(5))


if __name__ == "__main__":
    main()
