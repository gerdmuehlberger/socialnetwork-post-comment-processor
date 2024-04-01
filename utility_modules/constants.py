from utility_modules import parsers
from dash import Dash

APP = Dash(__name__)
CLI_ARGUMENTS = parsers.parse_cli_arguments()
HOST = parsers.HostParser().parse_url(CLI_ARGUMENTS.url)
DOMAIN = parsers.DomainParser().parse_url(CLI_ARGUMENTS.url)