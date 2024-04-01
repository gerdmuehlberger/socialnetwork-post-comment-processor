from utility_modules import utils

CLI_ARGUMENTS = utils.parse_cli_arguments()
HOST = utils.HostParser().parse_url(CLI_ARGUMENTS.url)
DOMAIN = utils.DomainParser().parse_url(CLI_ARGUMENTS.url)