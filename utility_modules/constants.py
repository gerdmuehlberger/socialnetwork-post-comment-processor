from utility_modules import utils

cliArguments = utils.parse_cli_arguments()
host = utils.HostParser().parse_url(cliArguments.url)
domain = utils.DomainParser().parse_url(cliArguments.url)