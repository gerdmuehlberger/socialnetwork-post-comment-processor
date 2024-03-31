from abc import ABC, abstractmethod
import json


class CredentialsConfigurator(ABC):
    def __init__(self) -> None:
        self.config_json = {}

    @abstractmethod
    def set_credentials(self) -> None:
        pass


class RedditCredentialSetup(CredentialsConfigurator):
    def __init__(self) -> None:
        super().__init__()
    
    def set_credentials(self) -> None:
        credentials ={}
        print("Please enter your reddit use script:")
        use_script = input()
        credentials['reddit_use_script'] = use_script
        
        print("Please enter your reddit client secret:")
        client_secret = input()
        credentials['reddit_client_secret'] = client_secret

        print("Please enter your reddit user agent:")
        user_agent = input()
        credentials['reddit_user_agent'] = user_agent

        print("Please enter your reddit username:")
        username = input()
        credentials['reddit_username'] = username

        print("Please enter your reddit password:")
        password = input()
        credentials['reddit_password'] = password

        with open('./config/reddit_config.json', 'w') as config_file:
            json.dump(credentials, config_file)


class YoutubeCredentialSetup(CredentialsConfigurator):
    def __init__(self) -> None:
        super().__init__()

    def set_credentials(self) -> None:
        credentials = {}
        print("Please enter your youtube API key.")
        api_key = input()
        credentials['youtube_api_key'] = api_key
        
        with open('./config/youtube_config.json', 'w') as config_file:
            json.dump(credentials, config_file)
